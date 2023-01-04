from django.db import models

# Create your models here.

class SpectralIndex(models.Model):
    spectral_index_name = models.TextField(db_column='spectral_index_name', default="")
    spectral_index_color_palette = models.TextField(db_column='spectral_index_color_palette', default="")
    bucket_name = models.TextField(db_column='bucket_name', default="")

    def serialize(self):
        return {
            "spectral_index_name": self.spectral_index_name,
            "spectral_index_color_palette": self.spectral_index_color_palette,
            "bucket_name": self.bucket_name
        }

class Imagery(models.Model):
    image_id = models.AutoField(db_column='image_id', primary_key=True)
    image_name = models.CharField(max_length=200, default="")
    spectral_index_name = models.TextField(db_column='spectral_index_name', default="")
    spectral_index_color_palette = models.TextField(db_column='spectral_index_color_palette', default="")
    spectral_index_name_palette = models.ForeignKey(SpectralIndex, related_name = 'spectral_index_name_palette', on_delete=models.CASCADE, null=True)
    spectral_index_equation = models.TextField(db_column='spectral_index_equation', default="")
    mei = models.TextField(db_column='mei', default="mei")
    vigs = models.TextField(db_column='vigs', default="vigs")
    pqkmeans = models.TextField(db_column='pqkmeans', default="pqkmeans")
    kmeans = models.TextField(db_column='kmeans', default="kmeans")
    pqkmeans_labels = models.TextField(db_column='pqkmeans_labels', default="")
    kmeans_labels = models.TextField(db_column='kmeans_labels', default="")
    shapefile_path_shp = models.FileField(upload_to= 'shapefiles', blank=True, null=True)
    shapefile_path_dbf = models.FileField(upload_to= 'shapefiles', blank=True, null=True)
    shapefile_path_sbn = models.FileField(upload_to= 'shapefiles', blank=True, null=True)
    shapefile_path_shx = models.FileField(upload_to= 'shapefiles', blank=True, null=True)
    shapefile_path_sbx = models.FileField(upload_to= 'shapefiles', blank=True, null=True)
    shapefile_path_prj = models.FileField(upload_to= 'shapefiles', blank=True, null=True)
    band_stack_list = models.TextField(db_column='band_stack_list', max_length=300, default="")
    k_value = models.TextField(db_column='k_value', max_length=30, default="3")
    num_subdimensions = models.TextField(db_column='num_subdimensions', max_length=30, default="1")
    ks_value = models.TextField(db_column='ks_value', max_length=30, default="256")
    sample_size = models.TextField(db_column='sample_size', max_length=30, default="500")
    bucket_name = models.TextField(db_column='bucket_name', default="")


    def serialize(self):
        return {"image_id": self.image_id, "image_name": self.image_name, "shapefile": self.shapefile_path_shp.path, "mei": self.mei, "vigs": self.vigs, "pqkmeans": self.pqkmeans, "kmeans": self.kmeans, "pqkmeans_labels": self.pqkmeans_labels, "kmeans_labels": self.kmeans_labels, "spectral_index_name": self.spectral_index_name, "spectral_index_color_palette":self.spectral_index_color_palette, "spectral_index_equation": self.spectral_index_equation, "band_stack_list": self.band_stack_list, "k_value":self.k_value, "num_subdimensions":self.num_subdimensions, "ks_value":self.ks_value, "sample_size":self.sample_size, "bucket_name": self.bucket_name}
