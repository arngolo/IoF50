# from operator import imatmul
from django.shortcuts import render
from django.http import JsonResponse
from .models import Imagery
import ee, os, json
import numpy as np
# from rasterio import features, mask
from django.views.decorators.csrf import csrf_exempt
# import geopandas as gpd
from affine import Affine
from .pqkmeans_imagery import PQKMeansGen
from .shapefile_to_json import shp_to_json
from osgeo import gdal
from .upload_to_server import upload_objects_to_gcp
import gdal2tiles
from .spectral_tools import normalized_difference, vigs_index, moisture_enhanced_index, save_spectral_index, get_metadata, get_bands
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
          shape_files = request.FILES.getlist('ShapefileLocation')

          if shape_files:
               # remove the existing shapefile from media 
               shapefiles = project_directory + '/media/shapefiles'
               if os.path.exists(shapefiles):
                    if len(os.listdir(shapefiles)) != 0:
                         for f in os.listdir(shapefiles):
                              os.remove(os.path.join(shapefiles, f))

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
               
               database = Imagery.objects.all()
               images = [image for image in database.all()]
               return JsonResponse([image.serialize() for image in images], safe=False)

     elif request.method == "PUT":
          # for this project, the database needs to have at least 1 element. index function creates 1 by default.
          image_update = Imagery.objects.get(pk=1)
          fetched_data = json.loads(request.body) #gets json data from the webpage (body as refered in javascript code). javascript uses "PUT" method of fetch to update the webpage contant
          image_name = fetched_data.get("image_name")
          image_update.image_name=image_name
          print(fetched_data.get("image_name"))
          image_update.save()

          # get shapefile path (from media /media/file) 
          vector_path = image_update.shapefile_path_shp.path
          if "\\" in vector_path:
               vector_path = vector_path.replace("\\", "/")

          # print(vector_path)

          # from shapefile to json
          data = shp_to_json(vector_path)
          # print(data)

          coordinates_list = data['geometry']['coordinates']
          geometry_json = ee.Geometry.MultiPolygon(coordinates_list, None, False)

          # get image, clip to the extent of the vector and mask its pixel values
          image = ee.Image(image_name).select(['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10'])

          # cliping
          mask = image.clip(geometry_json).mask()
          ## masking
          masked_image = image.updateMask(mask)

          # get masked image bounds
          bounds = image.select("B2").mask().gt(0).selfMask().addBands(1).reduceToVectors(reducer= ee.Reducer.first(), geometry = geometry_json, scale= 30, geometryType= "bb")

          # pixels to numpy arrays: to sample the pixels from the satellite image (number of pixels must be <= 262144):
          band_arrays = masked_image.sampleRectangle(region=bounds, defaultValue=0)
          mission = "landsat"
          
          bands = get_bands(mission, band_arrays)
          print(bands)

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
          # custom metadata
          metadata = get_metadata(bands["blue"], crs, affine_transform)

          # imput for pqkmeans
          output = project_directory + '/media/output_images'
          if not os.path.exists(output):
               os.mkdir(output)
          output = output + "/map.tif"

          # if normalized_index:
          #      # name = get_name()
          #      normalized_index = normalized_difference(bands["red"], bands["nir"])
          #      # metadata = get_metadata(np_arr_b1)
          #      # save normalized_index index
          #      output = project_directory + '/media/output_images/normalized_index.tif'
          #      color_text = "get color text from form"
          #      save_spectral_index(normalized_index, output, metadata)

          #      # grayscale to color ramp
          #      CMD = "gdaldem color-relief " + output + " " + color_text + " " + "-alpha" + output.split(".")[0] + "_colored.tif"
          #      os.system(CMD)
          #      output = output.split(".")[0] + "_colored.tif"
               
          # elif vigs:
          #      name = "vigs"
          #      vigs = vigs_index(bands["green"], bands["red"], bands["nir"], bands["swir1"], bands["swir2"])
          #      # save vigs index
          #      output = project_directory + '/media/output_images/vigs.tif'
          #      color_text = "get color text from form"
          #      save_spectral_index(vigs, output, metadata)

          #      # grayscale to color ramp
          #      CMD = "gdaldem color-relief " + output + " " + color_text + " " + "-alpha" + output.split(".")[0] + "_colored.tif"
          #      os.system(CMD)
          #      output = output.split(".")[0] + "_colored.tif"

          # elif mei:
          #      name = "mei"
          #      mei = moisture_enhanced_index(bands["coastal_aerosol"], bands["green"], bands["nir"], bands["swir1"])
          #      # save mei index
          #      output = project_directory + '/media/output_images/mei.tif'
          #      color_text = "get color text from form"
          #      save_spectral_index(mei, output, metadata)

          # elif pqkmeans:
          name = "lulc"
          k=3
          num_subdim=1
          Ks=256
          sample_size = 500
          color_text = project_directory + '/media/palette_color_text/color_text_file_pqkmeans.txt'
          PQKMeansGen([bands["blue"], bands["green"], bands["red"]], output, k, num_subdim, Ks, sample_size, metadata)

          # grayscale to color ramp
          CMD = "gdaldem color-relief " + output + " " + color_text + " " + "-alpha" + " " + output.split(".")[0] + "_colored.tif"
          os.system(CMD)

          # Generate maptiles
          input = output.split(".")[0] + "_colored.tif"
          # tiles_output = output.split(".")[0] + "_tiles"
          gdal2tiles.generate_tiles(input, project_directory + "/media/output_images/" + name, zoom='0-15', srcnodtata = 0)

          # upload maptiles to google cloud storage
          upload_objects_to_gcp(project_directory, authentication["bucket_name"], name)

          ## expose updated data again to the url
          database = Imagery.objects.all()
          images = [image for image in database.all()]
          return JsonResponse([image.serialize() for image in images], safe=False)
