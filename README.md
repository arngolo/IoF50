# IoF50 (Imagery on the Fly)
Primarily devised for Geospatial technology users, this website allows spatial analysis on the fly using GEE python API. It reduces user's computational costs, is memory efficient and users do not require a high storage capacity since the output result is primarely stored in local then uploaded to google cloud storage (GCS). 

## requirements
### windows
python3.7 (create a virtual env with python 3.7).
pip install -r requirements.txt (windows amd 64 bits).
[Microsoft Build Tolls](https://www.microsoft.com/en-us/download/details.aspx?id=48159) for pqkmeans installation. 2015 version used in this project. Try a recent version.
### Mac
brew install cmake
python3.7 (create a conda env with python 3.7):
- conda install -c conda-forge libgdal
- conda install -c conda-forge gdal
- pip install -r requirements_mac.txt

## GEE python authentication

Create a service account (first create a google cloud project from the developer IDE (assets section)):

On the project name click the home button, select the cloud console menu > `IAM & admins` > service accounts > `create service account`.

Create and download a JSON private key file for the service account.

### To authenticate:
- Place the private key in the root location of this project.
- From google cloud products choose storage and create a bucket to store your data. Give necessary permissions to your objects (public access): In the list of buckets, check the bucket box, click permissions:

`add principals:` allUsers
`assigned roles:` storage legacy bucket owner, reader; object owner, reader.

- In the `authentication.json` file, add the service account, the private key file name and the bucket name.

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
`LANDSAT/LC09/C02/T1/LC09_108030_20220909` (use with shapefile Sapporo)
`COPERNICUS/S2_SR/20220805T012659_20220805T013242_T54TWN` (use with shapefile Sapporo)

**Note:** GEE python API only accepts sampling <= 262144 pixels (the process of getting pixels from GEE cloud storage). For larger areas you might have to choose a shapefile with a higher level of administrative boundaries of your area of interest (`Sapporo for example in test_data folder`) or divide it into smaller pieces to meet the sampling requirements (`Lobito shapefile for example in test_data folder`).

## Get Spectral Index
For spectral index calculator, make sure you understand the satellite image specs (Bands). Only NASA Landsat and ESA Sentinel2 images allowed).

## Image Classification

- **Stack Bands:** list of bands to be stacked for unsupervised classification.

- **k:** as you wish for the number of clusters

- **num_of_subdim (M):**  The  number of subdimensions (from the input nD image) for quantization. Needs to be mltiple of num of bands. The higher the subdimension the slower the algorithm.

- **Ks:**  represents the maximum digital number. By default it is 256 that corresponds to 8 bits.

- **sample_size:** The number of pixels you select for quantization.

## ToDo
- Clear database. Clear output images from local.
- Check GCS's bucket/object content (spectral indices) and update in database (SpectralIndex table).
- Ask to save output image somewhere else before a new image is classified.
- Fix warning message on put request (currently requires page refresh).
- Explore Atmospheric correction and radiometric calibration for a better classification.
