# Imagery on the Fly (IoF)
Primarily devised for Geospatial technology users, this website allows spatial analysis on the fly using GEE python API. It reduces user's computational costs, is memory efficient and users do not require a high storage capacity since the output result is primarely stored in local then uploaded to google cloud storage (GCS). 

## requirements
python3.7 (create a virtual env with python 3.7)

### windows
pip install requirements.txt (windows)
[Microsoft Build Tolls](https://www.microsoft.com/en-us/download/details.aspx?id=48159) for pqkmeans.2015 version used in this project. Try a recent version.
### Mac
pip install django
pip install earthengine-api --upgrade
pip install pandas
pip install rasterio
pip install pqkmeans
pip install gdal2tiles
pip install google-cloud-storage
pip install pyproj

## GEE python authentication

Create a service account (first create a google cloud project from the developer IDE (assets section)).

On the project name click the home button, select the cloud console menu > `IAM & admins` > service accounts > `create service account`.

Create and download a JSON private key file for the service account.

### To authenticate:
- Place the private key in the root location of this project.
- In the `authentication.json` file, add the service account and the private key file name.

## uplaod local 
### maptiles generation
To upload local geotiff files, we have to first produce maptiles.
gdal (`gdal2files`) is used to produce tiles stored in a `<maptiles_folder>` that contains subfolders for different zoom levels.

### upload maptiles
Generated maptiles for this project are hosted in google cloud storage, uploaded using the google-cloud-storage API (API different from earthengine-api, so, authentication process is different but using the same private-key). After uploading a maptile we can have access to it as layer by using the public url `https://storage.googleapis.com/<bucket_name>/<folder_name>/{z}/{x}/{y}.png`. 
**Note:** Make sure to make your bucket and its objects (folders, files) public and set `owner` permissions for `allUsers` from google cloud storage.

## Usage
### Load area
Global shapefiles (for area to be analised) can be downloaded from [Diva GIS](https://www.diva-gis.org/Data) at different levels and used as input.
Shapfiles should be uploaded with its corresponding `.dbf, .sbn, .shx, .sbx, .prj` files at once. Use the data from `test_data` folder to test this application.

## Load Satellite Image
Satellite images ID should follow the format: `LANDSAT/<mission>/<collection>/<tier>/<image_ID>` for landsat and `COPERNICUS/<sentinel_mission>_<optional_processing_level>/<image_ID>` for sentinel. (check image ID availability from [example script](https://code.earthengine.google.com/848200c362694900b6027b30b0e99677) using `ee.ImageCollection`).

### Example:
`LANDSAT/LC09/C02/T1/LC09_182066_20220611` (use with shapefile Patrice_Lumumba)
`LANDSAT/LC09/C02/T1/LC09_182068_20220611` (use with shapefile Lobito)
`COPERNICUS/S2_SR/20220805T012659_20220805T013242_T54TWN` (use with shapefile Sapporo)

**Note:** GEE python API only accepts sampling <= 262144 pixels (the process of getting pixels from GEE cloud storage). For larger areas you might have to choose a shapefile with a higher level of administrative boundaries of your area of interest (`Sapporo for example in test_data folder`) or divide it into smaller pieces to meet the sampling requirements (`Lobito shapefile for example in test_data folder`).

## Get Spectral Index
For spectral index calculator, make sure you understand the satellite image specs (Bands). Only NASA Landsat and ESA Sentinel2 images allowed).
