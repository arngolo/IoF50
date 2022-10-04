from django.db import models
from django.contrib.auth.models import AbstractUser
import numpy as np
from ndarraydjango.fields import NDArrayField

# Create your models here.

class Imagery(models.Model):
    image_id = models.AutoField(db_column='image_id', primary_key=True)
    image_name = models.CharField(max_length=200, default="[]")
    remote_image = models.TextField(db_column='remote_image', default="[]")
    # remote_image = NDArrayField(dtype=np.uint16, blank=True, null=True) #remote satellite image
    # local_image = models.ImageField(upload_to= 'images', blank=True, null=True) # image with extracted info from remote image
    image_details = models.CharField(max_length=300, default="[]")

    # class Meta:
    #     db_table = 'Imagery'

    def serialize(self):
        return {"image_id": self.image_id, "image_name": self.image_name, "remote_image": self.remote_image, "image_details": self.image_details}