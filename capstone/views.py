from django.shortcuts import render
from django.http import JsonResponse
from .models import Imagery
import json
# Create your views here.
def index(request):

     if not Imagery.objects.all():

          image = Imagery()
          image.save()

     return render(request, 'capstone/index.html')

def pixels_app(request):
     if request.method == "GET":
          database = Imagery.objects.all()
          images = [image for image in database.all()] ## all posts
          # print(images)

          return JsonResponse([image.serialize() for image in images], safe=False)

     elif request.method == "PUT":
          # for this project, the database needs to have at least 1 element. index function creates 1 by default.          
          fetched_data = json.loads(request.body) #gets json data from the webpage (body as refered in javascript code). javascript uses "PUT" method of fetch to update the webpage contant
          print(fetched_data.get("remote_image"))


