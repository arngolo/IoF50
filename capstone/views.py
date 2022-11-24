# from operator import imatmul
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Imagery
import ee, os, json
import numpy as np
# from rasterio import features, mask
from django.views.decorators.csrf import csrf_exempt
# import geopandas as gpd
from affine import Affine
from .classifier import PQKMeansGen, KMeansGen
from .shapefile_to_json import shp_to_json
from osgeo import gdal
from .upload_to_server import upload_objects_to_gcp
import gdal2tiles
from .spectral_tools import normalized_difference, vigs_index, moisture_enhanced_index, save_spectral_index, get_metadata, get_bands, get_band_stack
from pyproj import Proj



# Earth Engine authentication
authentication = json.load(open(os.getcwd() + '/authentication.json'))
private_key = os.getcwd() + "/" + authentication["private_key"]
ee_credentials = ee.ServiceAccountCredentials(authentication["service_account"], private_key)
ee.Initialize(ee_credentials)

# google cloud storage authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = private_key

# Create your views here.
def index(request):
     if not Imagery.objects.all():

          image = Imagery()
          image.save()

     return render(request, 'capstone/index.html')

@csrf_exempt
def pixels_app(request):
     project_directory = os.getcwd()
     if request.method == "GET":
          database = Imagery.objects.all()
          images = [image for image in database.all()] ## all images
          # print(images)
          return JsonResponse([image.serialize() for image in images], safe=False)
     
     elif request.method == "POST":
          image_update = Imagery.objects.get(pk=1)

          if request.FILES.getlist('ShapefileLocation'):
               shape_files = request.FILES.getlist('ShapefileLocation')

               # remove the existing shapefile from media 
               shapefiles_folder = project_directory + '/media/shapefiles'
               if os.path.exists(shapefiles_folder):
                    if len(os.listdir(shapefiles_folder)) != 0:
                         for f in os.listdir(shapefiles_folder):
                              os.remove(os.path.join(shapefiles_folder, f))

               # # add new shapefile
               for file in shape_files:
                    if ".shp" in str(file):
                         print(str(file))    
                         image_update.shapefile_path_shp = file
                    elif ".dbf" in str(file):
                         print(str(file))    
                         image_update.shapefile_path_dbf = file
                    elif ".shx" in str(file):
                         print(str(file))    
                         image_update.shapefile_path_shx = file
                    elif ".sbx" in str(file):
                         print(str(file))    
                         image_update.shapefile_path_sbx = file
                    elif ".sbn" in str(file):
                         print(str(file))    
                         image_update.shapefile_path_sbn = file
                    elif ".prj" in str(file):
                         print(str(file))    
                         image_update.shapefile_path_prj = file

          # if the following condition is not true, returns False
          elif request.POST.get('SatelliteImage', False):
               sat_image = request.POST['SatelliteImage']
               image_update.image_name = sat_image

          elif request.POST.get('SpectralIndexName', False) and request.POST.get('SpectralIndexEquation', False):
               spectral_index_name = request.POST['SpectralIndexName']
               spectral_index_equation = request.POST['SpectralIndexEquation']
               image_update.spectral_index_name = spectral_index_name
               image_update.spectral_index_equation = spectral_index_equation

          elif request.POST.get('mei', False):
               mei = request.POST['mei']
               image_update.mei = mei

          elif request.POST.get('vigs', False):
               vigs = request.POST['vigs']
               image_update.vigs = vigs

          elif request.POST.get('BandStackList', False):
               band_stack_list = request.POST['BandStackList']
               image_update.band_stack_list = band_stack_list
          else:
               return exit(1)

          image_update.save()
          return HttpResponseRedirect(reverse("index"))

     elif request.method == "PUT":
          # for this project, the database needs to have at least 1 element. index function creates 1 by default.
          image_update = Imagery.objects.get(pk=1)
          fetched_data = json.loads(request.body) #gets json data from the webpage (body as refered in javascript code). javascript uses "PUT" method of fetch to update the webpage contant

          image_name = fetched_data.get("image_name")
          if image_name:
               image_update.image_name=image_name
               image_update.save()
          else:
               image_name = image_update.image_name
          print("\n","image name: ",image_name)

          #satellite mission
          if image_name.startswith("LANDSAT"):
               mission = 'landsat'
          elif image_name.startswith("COPERNICUS"):
               mission = 'sentinel'
          print("\n","Satellite Mission: ", mission, "\n")

          spectral_index_name = fetched_data.get("spectral_index_name")
          spectral_index_equation = fetched_data.get("spectral_index_equation")
          mei = fetched_data.get("mei")
          vigs = fetched_data.get("vigs")
          pqkmeans = fetched_data.get("pqkmeans")
          kmeans = fetched_data.get("kmeans")
          band_stack_list = fetched_data.get("band_stack_list")


          print("\n","spectral index name: ",spectral_index_name)
          print("\n","spectral index equation: ",spectral_index_equation)
          print("\n","mei: ",mei)
          print("\n","vigs: ",vigs)
          print("\n","pqkmeans: ",pqkmeans)
          print("\n","kmeans: ",kmeans)
          
          # get shapefile path (from media /media/file) 
          vector_path = image_update.shapefile_path_shp.path
          if "\\" in vector_path:
               vector_path = vector_path.replace("\\", "/")

          # from shapefile to json
          data = shp_to_json(vector_path)
          # print(data)

          coordinates_list = data['geometry']['coordinates']
          geometry_json = ee.Geometry.MultiPolygon(coordinates_list, None, False)

          # get image, clip to the extent of the vector and mask its pixel values
          image = ee.Image(image_name)

          # cliping
          mask = image.clip(geometry_json).mask()
          ## masking
          masked_image = image.updateMask(mask)

          # get masked image bounds
          bounds = image.select("B2").mask().gt(0).selfMask().addBands(1).reduceToVectors(reducer= ee.Reducer.first(), geometry = geometry_json, scale= 30, geometryType= "bb")

          # pixels to numpy arrays: to sample the pixels from the satellite image (number of pixels must be <= 262144):
          band_arrays = masked_image.sampleRectangle(region=bounds, defaultValue=0)
          
          bands = get_bands(mission, band_arrays)
          # print(bands)

          # IMAGE METADATA
          image_info=image.getInfo()
          crs = image_info["bands"][0]["crs"]
          crs_transform = image_info["bands"][0]["crs_transform"]
          # get top(north), left(west) bounds of the masked image
          bbox = bounds.getInfo()["features"][0]["geometry"]["coordinates"][0]
          west = bbox[0][0]
          north = bbox[2][1]
          # convert from decimal to UTM
          myProj = Proj(crs)
          left,top = myProj(west, north)
          print("left bound: ", left, "\n", "top bound: ", top)
          # affine transformation in the following format: (scale, shear, translation, scale, shear, translation)
          affine_transform = Affine(crs_transform[0], crs_transform[1], left, crs_transform[3], crs_transform[4], top)
          if mission == "sentinel":
               affine_transform = Affine(10, crs_transform[1], left, crs_transform[3], -10, top)

          print("Affine Transformation: ", affine_transform)
          # custom metadata
          metadata = get_metadata(bands["B2"], crs, affine_transform)

          # images output directory
          output = project_directory + '/media/output_images'
          if not os.path.exists(output):
               os.mkdir(output)

          if spectral_index_name and spectral_index_equation:
               name = spectral_index_name
               #get_bands function also gets spectral index
               spectral_index = get_bands(mission, band_arrays, spectral_index_equation)
               # save normalized_index index
               output = project_directory + '/media/output_images/' + spectral_index_name + '.tif'
          #      color_text = "get color text from form"
               color_text = project_directory + '/media/palette_color_text/color_text_file_orange_green.txt'
               save_spectral_index(spectral_index, output, metadata)
               
          elif vigs:
               if mission == "landsat":
                    name = "vigs"
                    vigs = vigs_index(bands["B3"], bands["B4"], bands["B5"], bands["B6"], bands["B7"])
                    # save vigs index
                    output = project_directory + '/media/output_images/vigs.tif'
                    # color_text = "get color text from form"
                    color_text = project_directory + '/media/palette_color_text/color_text_file_orange_green.txt'
                    save_spectral_index(vigs, output, metadata)
               else:
                    pass

          elif mei:
               if mission == "landsat":
                    name = "mei"
                    mei = moisture_enhanced_index(bands["B1"], bands["B3"], bands["B5"], bands["B6"])
                    # save mei index
                    output = project_directory + '/media/output_images/mei.tif'
                    # color_text = "get color text from form"
                    color_text = project_directory + '/media/palette_color_text/color_text_file_orange_green.txt'
                    save_spectral_index(mei, output, metadata)
               else:
                    pass

          elif pqkmeans and band_stack_list:
               name = "lulc_pqkmeans"
               k=3
               num_subdim=1
               Ks=256
               sample_size = 500
               output = project_directory + '/media/output_images/map_pqkmeans.tif'
               color_text = project_directory + '/media/palette_color_text/color_text_file_pqkmeans.txt'
               band_stack = get_band_stack(bands, band_stack_list, project_directory)
               PQKMeansGen(band_stack, output, k, num_subdim, Ks, sample_size, metadata)

          elif kmeans and band_stack_list:
               name = "lulc_kmeans"
               k=3
               output = project_directory + '/media/output_images/map_kmeans.tif'
               color_text = project_directory + '/media/palette_color_text/color_text_file_pqkmeans.txt'
               band_stack = get_band_stack(bands, band_stack_list, project_directory)
               KMeansGen(band_stack, output, k, metadata)

          else:
               return exit(1)
          # grayscale to color ramp
          CMD = "gdaldem color-relief " + output + " " + color_text + " " + "-alpha" + " " + output.split(".")[0] + "_colored.tif"
          os.system(CMD)

          # Generate maptiles
          input = output.split(".")[0] + "_colored.tif"
          # tiles_output = output.split(".")[0] + "_tiles"
          gdal2tiles.generate_tiles(input, project_directory + "/media/output_images/" + name, zoom='0-15', srcnodtata = 0)

          # upload maptiles to google cloud storage
          upload_objects_to_gcp(project_directory, authentication["bucket_name"], name)

          return HttpResponseRedirect(reverse("index"))
