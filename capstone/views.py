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
from .upload_to_server import upload_objects_to_gcp
import gdal2tiles


# Earth Engine authentication
authentication = json.load(open(os.getcwd() + '/authentication.json'))
private_key = os.getcwd() + "/" + authentication["private_key"]
ee_credentials = ee.ServiceAccountCredentials(authentication["service_account"], private_key)
ee.Initialize(ee_credentials)

# google cloud storage authentication
import os
from google.cloud import storage
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = private_key

# Create your views here.
def index(request):
     if not Imagery.objects.all():

          image = Imagery()
          image.save()

     return render(request, 'capstone/index.html')

@csrf_exempt
def pixels_app(request):
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
               media_files = os.getcwd() + '/media/media_files'
               if os.path.exists(media_files):
                    if len(os.listdir(media_files)) != 0:
                         for f in os.listdir(media_files):
                              os.remove(os.path.join(media_files, f))

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
          image = ee.Image("LANDSAT/LC09/C02/T1/LC09_182066_20220611").select(['B2', 'B3', 'B4'])
          # cliping
          mask = image.clip(geometry_json).mask()
          ## masking
          masked_image = image.updateMask(mask)

          # pixels to numpy arrays:
          band_arrays = masked_image.sampleRectangle(region=geometry_json, defaultValue=0)
          b2 = band_arrays.get("B2")
          np_arr_b2 = np.array(b2.getInfo())

          b3 = band_arrays.get("B3")
          np_arr_b3 = np.array(b3.getInfo())

          b4 = band_arrays.get("B4")
          np_arr_b4 = np.array(b4.getInfo())

          bands = [np_arr_b2, np_arr_b3, np_arr_b4]
          print(bands)

          # image metadata
          image_info=image.getInfo()
          crs = image_info["bands"][0]["crs"]
          crs_transform = image_info["bands"][0]["crs_transform"]
          # affine transformation is in the following format: (scale, shear, translation, scale, shear, translation)
          affine_transform = Affine(crs_transform[0], crs_transform[1], crs_transform[2], crs_transform[3], crs_transform[4], crs_transform[5])

          meta_out = {'driver': 'GTiff',
          'dtype': 'float32',
          'nodata': -3.402823e+38,
          'width': np_arr_b2.shape[1],
          'height': np_arr_b2.shape[0],
          'count': 3,
          'crs': crs,
          'transform': affine_transform}

          # imput for pqkmeans
          output = os.getcwd() + '/media/output_images'
          if not os.path.exists(output):
               os.mkdir(output)
          output = output + "/map.tif"
          
          k=3
          num_subdim=1
          Ks=256
          sample_size = 500

          PQKMeansGen(bands, output, k, num_subdim, Ks, sample_size, meta_out)

          # Generate maptiles
          gdal2tiles.generate_tiles(output, authentication["maptiles_directory"], zoom='0-15', srcnodtata = 0)

          # upload maptiles to google cloud storage
          upload_objects_to_gcp(authentication["bucket_name"], authentication["maptiles_directory"])

          ## expose updated data again to the url
          database = Imagery.objects.all()
          images = [image for image in database.all()]
          return JsonResponse([image.serialize() for image in images], safe=False)
