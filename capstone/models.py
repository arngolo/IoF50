from django.db import models

# Create your models here.

class Imagery(models.Model):
    image_id = models.AutoField(db_column='image_id', primary_key=True)
    image_name = models.CharField(max_length=200, default="[]")
    remote_image = models.TextField(db_column='remote_image', default="[]")
    shapefile_path = models.FileField(upload_to= 'media_files', blank=True, null=True)
    image_details = models.CharField(max_length=300, default="[]")

    def serialize(self):
        return {"image_id": self.image_id, "image_name": self.image_name, "remote_image": self.remote_image, "shapefile": self.shapefile_path.path, "image_details": self.image_details}