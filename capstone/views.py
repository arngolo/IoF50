# from operator import imatmul
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Imagery, SpectralIndex
import ee, os, json
# import numpy as np
# from rasterio import features, mask
from django.views.decorators.csrf import csrf_exempt
# import geopandas as gpd
from affine import Affine
from .classifier import PQKMeansGen, KMeansGen
from .shapefile_to_json import shp_to_json
# from osgeo import gdal
from .upload_to_server import upload_objects_to_gcp
import gdal2tiles
from .spectral_tools import vigs_index, moisture_enhanced_index, save_spectral_index, get_metadata, get_bands, get_band_stack
from pyproj import Proj
from django.contrib import messages



# Earth Engine authentication
try:
     authentication = json.load(open(os.getcwd() + '/authentication.json'))
     private_key = os.getcwd() + "/" + authentication["private_key"]
     ee_credentials = ee.ServiceAccountCredentials(authentication["service_account"], private_key)
     ee.Initialize(ee_credentials)
except Exception as Err:
     messages.error(message = Err)

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
          print(images)
          return JsonResponse([image.serialize() for image in images], safe=False)
     
     elif request.method == "POST":
          image_update = Imagery.objects.get(pk=1)

          if request.FILES.getlist('ShapefileLocation') or request.FILES.getlist('Shapefileparentdir'):
               try:
                    if request.FILES.getlist('ShapefileLocation'):
                         shape_files = request.FILES.getlist('ShapefileLocation')
                    elif request.FILES.getlist('Shapefileparentdir'):
                         shape_files = request.FILES.getlist('Shapefileparentdir')

                    # remove the existing shapefile from media
                    shapefiles_folder = project_directory + '/media/shapefiles'
                    # try:
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
                         image_update.save()
                    messages.success(request, 'shapfiles saved')
               except Exception as Err:
                    messages.error(request, Err)

          # if the following condition is not true, returns False
          elif request.POST.get('SatelliteImage', False):
               try:
                    sat_image = request.POST['SatelliteImage']
                    image_update.image_name = sat_image
                    messages.success(request, 'image ID saved')
               except Exception as Err:
                    messages.error(request, Err)

          elif request.POST.get('SpectralIndexName', False) and request.POST.get('SpectralIndexEquation', False) and request.POST.get('SpectralIndexColorPalette', False) or request.POST.get('SpectralIndexColorPalette', False):
               try:
                    spectral_index_name = request.POST['SpectralIndexName']
                    spectral_index_equation = request.POST['SpectralIndexEquation']
                    spectral_index_color_palette = request.POST['SpectralIndexColorPalette']
                    image_update.spectral_index_name = spectral_index_name
                    image_update.spectral_index_equation = spectral_index_equation
                    image_update.spectral_index_color_palette = spectral_index_color_palette

                    # save index name and color palette in spectral indices table
                    if request.POST.get('SpectralIndexName') != "":
                         try:
                              index_name_palette_save = SpectralIndex.objects.get(spectral_index_name=spectral_index_name)
                              # index_name_palette_save.spectral_index_color_palette = spectral_index_color_palette
                              # index_name_palette_save.save()
                              messages.error(request, spectral_index_name + ' index already exists')
                         except:
                              index_name_palette_save = SpectralIndex.objects.create(spectral_index_name=spectral_index_name, spectral_index_color_palette=spectral_index_color_palette)
                              index_name_palette_save.save()
                              messages.success(request, 'spectral index request info saved')

               except Exception as Err:
                    messages.error(request, Err)

          elif request.POST.get('mei', False):
               try:
                    mei = request.POST['mei']
                    image_update.mei = mei
                    messages.success(request, 'moisture enhanced index (mei) request info saved')
               except Exception as Err:
                    messages.error(request, Err)

          elif request.POST.get('vigs', False):
               try:
                    vigs = request.POST['vigs']
                    image_update.vigs = vigs
                    messages.success(request, 'vigs request info saved (vegetation index considering green and short-wave infrared)')
               except Exception as Err:
                    messages.error(request, Err)

          elif request.POST.get('BandStackList', False) and request.POST.get('KValue', False) and request.POST.get('NumSubdim', False) and request.POST.get('Ks', False) and request.POST.get('SampleSize', False):
               try:
                    band_stack_list = request.POST['BandStackList']
                    k_value = request.POST['KValue']
                    num_subdimensions = request.POST['NumSubdim']
                    ks_value = request.POST['Ks']
                    sample_size = request.POST['SampleSize']
                    image_update.band_stack_list = band_stack_list
                    image_update.k_value = k_value
                    image_update.num_subdimensions = num_subdimensions
                    image_update.ks_value = ks_value
                    image_update.sample_size = sample_size
                    messages.success(request, 'classifier parameters saved')
               except Exception as Err:
                    messages.error(request, Err)

          elif request.POST.get('clear_index', False):
               try:
                    index_name = request.POST['clear_index']
                    clear_index = SpectralIndex.objects.get(spectral_index_name=index_name)
                    clear_index.delete()
                    messages.success(request, index_name + ' index deleted from database')
               except Exception as Err:
                    messages.error(request, Err)


          else:
               messages.error(request, 'no request. requests are: load shapfile, insert image ID, calculate spectral index, calculate custom spectral index and classify image')
               return HttpResponseRedirect(reverse("index"))

          image_update.save()

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
          else:
               messages.error(request, 'please make sure you use landsat or sentinel2 data')
               return HttpResponseRedirect(reverse("index"))
          print("\n","Satellite Mission: ", mission, "\n")

          spectral_index_name = fetched_data.get("spectral_index_name")
          spectral_index_equation = fetched_data.get("spectral_index_equation")
          spectral_index_color_palette = fetched_data.get("spectral_index_color_palette")
          mei = fetched_data.get("mei")
          vigs = fetched_data.get("vigs")
          pqkmeans = fetched_data.get("pqkmeans")
          kmeans = fetched_data.get("kmeans")
          band_stack_list = fetched_data.get("band_stack_list")
          k_value = fetched_data.get("k_value")
          num_subdimensions = fetched_data.get("num_subdimensions")
          ks_value = fetched_data.get("ks_value")
          sample_size = fetched_data.get("sample_size")


          print("\n","spectral index name: ",spectral_index_name)
          print("\n","spectral index equation: ",spectral_index_equation)
          print("\n","spectral_index_color_palette: ",spectral_index_color_palette)
          print("\n","mei: ",mei)
          print("\n","vigs: ",vigs)
          print("\n","pqkmeans: ",pqkmeans)
          print("\n","kmeans: ",kmeans)
          
          # get unique (first ) shapefile path (from media: /media/shapefiles) 
          vector_path = image_update.shapefile_path_shp.path
          if "\\" in vector_path:
               vector_path = vector_path.replace("\\", "/")

          # get unique (first ) shapefile parent directory
          vector_parent_dir = os.path.dirname(vector_path)

          if not pqkmeans and not kmeans:
               # iterate over shapefile parent directory to perform imagery in all related
               for vector in os.listdir(vector_parent_dir):
                    if vector.endswith(".shp"):
                         vector_path = os.path.join(vector_parent_dir, vector)
                         print("VECTOR PATH", vector_path)
                         # from shapefile to json
                         try:
                              data = shp_to_json(vector_path)
                         except Exception as Err:
                              messages.error(request, Err)
                              return HttpResponseRedirect(reverse("index"))
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
                         try:
                              bands = get_bands(mission, band_arrays)
                         except Exception as Err:
                              messages.error(request, Err)
                              return HttpResponseRedirect(reverse("index"))
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
                              color_text = project_directory + '/media/palette_color_text/color_text_file_' + spectral_index_color_palette + '.txt'
                              save_spectral_index(spectral_index, output, metadata)

                         elif vigs:
                              if mission == "landsat":
                                   name = "vigs"
                                   vigs_indx = vigs_index(bands["B3"], bands["B4"], bands["B5"], bands["B6"], bands["B7"])
                                   # save vigs index
                                   output = project_directory + '/media/output_images/vigs.tif'
                                   color_text = project_directory + '/media/palette_color_text/color_text_file_' + spectral_index_color_palette + '.txt'
                                   save_spectral_index(vigs_indx, output, metadata)
                                   try:
                                        index_name_palette_save = SpectralIndex.objects.get(spectral_index_name=name)
                                        index_name_palette_save.spectral_index_color_palette = spectral_index_color_palette
                                        index_name_palette_save.save()
                                        messages.error(request, 'vigs ' + ' index already exists')
                                   except:
                                        index_name_palette_save = SpectralIndex.objects.create(spectral_index_name=name, spectral_index_color_palette=spectral_index_color_palette)
                                        index_name_palette_save.save()
                                   messages.success(request, 'vigs request info saved')
                              else:
                                   messages.error(request, 'vigs index is exclusiv for landsat data')
                                   return HttpResponseRedirect(reverse("index"))

                         elif mei:
                              if mission == "landsat":
                                   name = "mei"
                                   mei_indx = moisture_enhanced_index(bands["B1"], bands["B3"], bands["B5"], bands["B6"])
                                   # save mei index
                                   output = project_directory + '/media/output_images/mei.tif'
                                   color_text = project_directory + '/media/palette_color_text/color_text_file_' + spectral_index_color_palette + '.txt'
                                   save_spectral_index(mei_indx, output, metadata)
                                   try:
                                        index_name_palette_save = SpectralIndex.objects.get(spectral_index_name=name)
                                        index_name_palette_save.spectral_index_color_palette = spectral_index_color_palette
                                        index_name_palette_save.save()
                                        messages.error(request, 'mei ' + ' index already exists')
                                   except:
                                        index_name_palette_save = SpectralIndex.objects.create(spectral_index_name=name, spectral_index_color_palette=spectral_index_color_palette)
                                        index_name_palette_save.save()
                                   messages.success(request, 'mei request info saved')
                              else:
                                   messages.error(request, 'mei index is exclusiv for landsat data')
                                   return HttpResponseRedirect(reverse("index"))

                         # else:
                         #      messages.success(request, 'please check your spectral index calculation')
                         #      return HttpResponseRedirect(reverse("index"))

          if pqkmeans and band_stack_list:
               name = "lulc_pqkmeans"
               k = int(k_value)
               num_subdim = int(num_subdimensions)
               Ks = int(ks_value)
               sample_size = int(sample_size)
               output = project_directory + '/media/output_images/map_pqkmeans.tif'
               color_text = project_directory + '/media/palette_color_text/color_text_file_classifier.txt'
               band_stack, num_bands, crs, transform = get_band_stack(band_stack_list, project_directory)
               metadata = get_metadata(band_stack[0], crs, transform)
               print("BAND STACK 0", band_stack[0])
               print("meta crs: ",metadata['crs'])
               print("meta transform: ",metadata['transform'])
               if num_bands != len(band_stack_list.split(",")):
                    messages.error(request, 'Band or index not present. Please update band list')
                    return HttpResponseRedirect(reverse("index"))
               PQKMeansGen(band_stack, output, k, num_subdim, Ks, sample_size, metadata)

          elif kmeans and band_stack_list:
               name = "lulc_kmeans"
               k = int(k_value)
               output = project_directory + '/media/output_images/map_kmeans.tif'
               color_text = project_directory + '/media/palette_color_text/color_text_file_classifier.txt'
               band_stack, num_bands, crs, transform = get_band_stack(band_stack_list, project_directory)
               metadata = get_metadata(band_stack[0], crs, transform)
               print("BAND STACK 0", band_stack[0])
               print("meta crs: ",metadata['crs'])
               print("meta transform: ",metadata['transform'])
               print("num_bands: ", num_bands)
               print("band_stack_list: ", len(band_stack_list.split(",")))
               if num_bands != len(band_stack_list.split(",")):
                    messages.error(request, 'Band or index not present. Please update band list')
                    return HttpResponseRedirect(reverse("index"))
               KMeansGen(band_stack, output, k, metadata)

          # grayscale to color ramp
          CMD = "gdaldem color-relief " + output + " " + color_text + " " + "-alpha" + " " + output.split(".")[0] + "_colored.tif"
          os.system(CMD)

          # Generate maptiles
          input = output.split(".")[0] + "_colored.tif"
          # tiles_output = output.split(".")[0] + "_tiles"
          gdal2tiles.generate_tiles(input, project_directory + "/media/output_images/" + name, zoom='0-15', srcnodata = 0)

          # upload maptiles to google cloud storage
          upload_objects_to_gcp(project_directory, authentication["bucket_name"], name)
          messages.success(request, 'map generated successfully')

     return HttpResponseRedirect(reverse("index"))

def spectral_info(request):
     if request.method == "GET":
          infos = SpectralIndex.objects.all()
          infos = [image for image in infos.all()] ## all images
          # print(images)
          return JsonResponse([info.serialize() for info in infos], safe=False)
