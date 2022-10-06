from django.shortcuts import render
from django.http import JsonResponse
from .models import Imagery
import json
from django.views.decorators.csrf import csrf_exempt

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

     elif request.method == "PUT":
          # for this project, the database needs to have at least 1 element. index function creates 1 by default.
          image_update = Imagery.objects.get(pk=1)
          fetched_data = json.loads(request.body) #gets json data from the webpage (body as refered in javascript code). javascript uses "PUT" method of fetch to update the webpage contant
          remote_image = fetched_data.get("remote_image")
          image_update.remote_image=remote_image
          print(fetched_data.get("remote_image"))
          image_update.save()

          ## expose updated data again to the url
          database = Imagery.objects.all()
          images = [image for image in database.all()]
          return JsonResponse([image.serialize() for image in images], safe=False)
