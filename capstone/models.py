from django.db import models

# Create your models here.

class Imagery(models.Model):
    image_id = models.AutoField(db_column='image_id', primary_key=True)
    image_name = models.CharField(max_length=200, default="")
    spectral_index_name = models.TextField(db_column='spectral_index_name', default="")
    spectral_index_equation = models.TextField(db_column='spectral_index_equation', default="")
    mei = models.TextField(db_column='mei', default="mei")
    vigs = models.TextField(db_column='vigs', default="vigs")
    pqkmeans = models.TextField(db_column='pqkmeans', default="pqkmeans")
    kmeans = models.TextField(db_column='kmeans', default="kmeans")
    shapefile_path_shp = models.FileField(upload_to= 'shapefiles', blank=True, null=True)
    shapefile_path_dbf = models.FileField(upload_to= 'shapefiles', blank=True, null=True)
    shapefile_path_sbn = models.FileField(upload_to= 'shapefiles', blank=True, null=True)
    shapefile_path_shx = models.FileField(upload_to= 'shapefiles', blank=True, null=True)
    shapefile_path_sbx = models.FileField(upload_to= 'shapefiles', blank=True, null=True)
    shapefile_path_prj = models.FileField(upload_to= 'shapefiles', blank=True, null=True)
    # image_details = models.CharField(max_length=300, default="[]")

    def serialize(self):
        return {"image_id": self.image_id, "image_name": self.image_name, "shapefile": self.shapefile_path_shp.path, "mei": self.mei, "vigs": self.vigs, "pqkmeans": self.pqkmeans, "kmeans": self.kmeans, "spectral_index_name": self.spectral_index_name, "spectral_index_equation": self.spectral_index_equation}