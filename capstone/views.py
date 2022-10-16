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

# Earth Engine authentication
authentication = json.load(open(os.getcwd() + '/authentication.json'))
ee_credentials = ee.ServiceAccountCredentials(authentication["service_account"], os.getcwd() + "/" + authentication["private_key"])
ee.Initialize(ee_credentials)

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
          shape_file = request.FILES['ShapefileLocation']
          if shape_file:
               # remove the existing shapefile from media 
               media_files = os.getcwd() + '/media/media_files'
               # if "\\" in media_files:
               #      media_files = media_files.replace("\\", "/")
               if os.path.exists(media_files):
                    if len(os.listdir(media_files)) != 0:
                         for f in os.listdir(media_files):
                              os.remove(os.path.join(media_files, f))

               print("shapefile: ", shape_file)
               # add new shapefile
               image_update.shapefile_path = shape_file
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
          # try:
          vector_path = image_update.shapefile_path.path
          if "\\" in vector_path:
               vector_path = vector_path.replace("\\", "/")

          # vector = gpd.read_file(vector_path)
          # # except:
          # #      print("shapefile path not stored in database, shapefile is not stored in media files OR something else went wrong")
          
          # # change geometry to the same geometry as the image UTM zone north !
          # vector = vector.geometry.to_crs("EPSG:32633")
          # print(vector)

          # from shapefile to json
          data = shp_to_json(vector_path)
          print(data)

          # Get list of geometries for all features in vector file
          # geom = [shapes for shapes in vector.geometry]

          # # Read corresponding vector from json
          # Patrice_Lumumba_json = open('Patrice_Lumumba.json')
          # data = json.load(Patrice_Lumumba_json)

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
          output = output + "/test_out.tif"
          
          k=3
          num_subdim=1
          Ks=256
          sample_size = 500

          PQKMeansGen(bands, output, k, num_subdim, Ks, sample_size, meta_out)



          ## expose updated data again to the url
          database = Imagery.objects.all()
          images = [image for image in database.all()]
          return JsonResponse([image.serialize() for image in images], safe=False)
