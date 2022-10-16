from django.db import models

# Create your models here.

class Imagery(models.Model):
    image_id = models.AutoField(db_column='image_id', primary_key=True)
    image_name = models.CharField(max_length=200, default="[]")
    remote_image = models.TextField(db_column='remote_image', default="[]")
    shapefile_path_shp = models.FileField(upload_to= 'media_files', blank=True, null=True)
    shapefile_path_dbf = models.FileField(upload_to= 'media_files', blank=True, null=True)
    shapefile_path_sbn = models.FileField(upload_to= 'media_files', blank=True, null=True)
    shapefile_path_shx = models.FileField(upload_to= 'media_files', blank=True, null=True)
    shapefile_path_sbx = models.FileField(upload_to= 'media_files', blank=True, null=True)
    shapefile_path_prj = models.FileField(upload_to= 'media_files', blank=True, null=True)
    image_details = models.CharField(max_length=300, default="[]")

    def serialize(self):
        return {"image_id": self.image_id, "image_name": self.image_name, "remote_image": self.remote_image, "shapefile": self.shapefile_path_shp.path, "image_details": self.image_details}