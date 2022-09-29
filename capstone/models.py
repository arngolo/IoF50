from django.db import models
from django.contrib.auth.models import AbstractUser
import numpy as np
from ndarraydjango.fields import NDArrayField

# Create your models here.

class Imagery(models.Model):
    image_id = models.AutoField(db_column='image_id', primary_key=True)
    image_name = models.CharField(max_length=200, blank=True, null=True)
    remote_image = NDArrayField(shape=(32, 4), dtype=np.uint16, blank=True, null=True) #remote satellite image
    # remote_image = models.ImageField(blank=True, null=True) #remote satellite image
    local_image = models.ImageField(upload_to= 'images', blank=True, null=True) # image with extracted info from remote image
    image_details = models.CharField(max_length=300, blank=True, null=True)

    # class Meta:
    #     db_table = 'Imagery'

    def serialize(self):
        return {"image_id": self.image_id, "image_name": self.image_name, "remote_image": self.remote_image, "local_image": self.local_image, "image_details": self.image_details}