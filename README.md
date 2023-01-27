# IoF50 (Imagery on the Fly)
### Distinctiveness and Complexity
This project differs from other projects in this course because it explores some other technologies (APIs and libraries) not taught or implemented in other projects and the  general idea is a web map application devised for Geospatial technology users, allowing them to perform spatial analysis on the fly using Google Earth Engine (GEE) python API. Compared to usual geospatial softwares, this web map application reduces user's computational costs, is memory efficient and users do not require a high storage capacity since the output result is primarely stored in local then uploaded to Google Cloud Storage (GCS).

Its complexity is based on the fact that it goes beyond what was taught in the course, by combining different technologies, for example, the usage of  geospatial technology libraries such as Geospatial Data Abstraction library (GDAL) and rasterio (used for reading, writing and pre-processing raster and vector data), the usage of APIs such as GEE python API, to access NASA’s and European Space Agency's (ESA) satellite data, the usage of GCS to store the output of the analysis, as well as the implementation of some machine learning algorithms for image classification. 

Integrating all these different technologies is a challenging task bacause it requires some specific environments to run in different OS, as well as customisation of open source code to achieve the goal of the original idea.

## directories/files content
- **`capstone`**
  - `models.py` creates 2 tables: `Imagery`, to temporarily store all image and vector related information, and `SpectralIndex`, to permanentely store information about all created spectral indices.
  - `urls.py` contains 2 APIs urls: `pixels`, to expose data from Imagery table, and `spectral_info`, to expose data from SpectralIndex table.
  - `views.py` apart from GEE authentication lines of code, contains 3 views (functions): `index`, to create (if non-existent) or display the initial page, `pixels_app`, to perform image analisys through GET, POST and PUT requests, and `spectral_info`, to update SpectralIndex table.
  - `shapefile_to_json.py` a script to convert vector data from shapefile format to json format required for GEE API.  
  - `spectral_tools.py` a script with numerous pre-processing functions for satellite images such as, spectral index calculation, save spectral index, get image metadata, filter bands, image stack, image mosaic.  
  - `classifier.py` a script that contains 2 clustering algorithms: kmeans and a quantised version of kmeans: [pqkmeans](https://github.com/DwangoMediaVillage/pqkmeans).  
  - `upload_to_server.py` a script to upload local files (generated maptiles) to GCS.  
  - **`static>`**
    - **`capstone>`**
      - `leaflet.js` Leaflet library for web mapping.  
      - `leaflet.css` Leaflet CSS file.  
      - `ee_api_js.js` GEE javascript API for web mapping (not used in this branch).  
      - `index.js` main javascript file for the application.  
      - `style.css` main css styling file for the application.  
  - **`templates>`**
    - **`capstone>`**
      - `index.html` application main html file.  
      - `layout.html` html layout file.  
- **`final_project>`**
  - `settings.py` contains lines of code to handle `media` (external images and files) and django built in `message tags`.
- **`media>`**
  - **`output_images`** folder stores the output images generated during the analysis (initially empty).  
  - **`palette_color_text>`** folder contains the files used to create color palletes for spectral indices.  
    - `color_text_file_Blues.txt` customised color code for Blue color pallete.  
    - `color_text_file_bygor.txt` customised color code for Blue, Yellow, Green, Orange color pallete.  
    - `color_text_file_bygor2.txt` customised color code for Blue, Yellow, Green, Orange color pallete.  
    - `color_text_file_classifier.txt` customised color code for categorical color pallete.  
    - `color_text_file_divergingBrBG.txt` customised color code for Brown, Blue, Green color pallete.  
    - `color_text_file_Greens.txt` customised color code for Green color pallete.  
    - `color_text_file_orang_green.txt` customised color code for Orange, Green color pallete.  
    - `color_text_file_Oranges.txt` customised color code for Orange color pallete.  
    - `color_text_file_OrRd.txt` customised color code for Orange, Red color pallete.  
    - `color_text_file_PRGn.txt` customised color code for PRGn color pallete.  
    - `color_text_file_rainbow.txt` customised color code for Rainbow color pallete.  
    - `color_text_file_Reds.txt` customised color code for Red color pallete.  
    - `color_text_file_rgb.txt` customised color code for RGB color pallete.  
    - `color_text_file_Turbo.txt` customised color code for Turbo color pallete.  
    - `color_text_file_viridis.txt` customised color code for Viridis color pallete.  
  - **`shapefiles>`** folder stores the uploaded shapefiles (initially empty).  
  - **`default_shapefiles>`** folder contains a dummy shapefile that is loaded once the database is created.  
    - `dummy_shapefile.shp` dummy shapefile to be loaded in the database.  
    - `dummy_shapefile.dbf` dummy shapefile dependency file to be loaded in the database.  
    - `dummy_shapefile.prj` dummy shapefile dependency to be loaded in the database.  
    - `dummy_shapefile.sbn` dummy shapefile dependency to be loaded in the database.  
    - `dummy_shapefile.sbx` dummy shapefile dependency to be loaded in the database.  
    - `dummy_shapefile.shx` dummy shapefile dependency to be loaded in the database.  
- **`test_data>`** folder contains shapefiles of 3 different locations in the world to test the application.  
  - `Lobito` folder contains  shapefiles of Lobito area in Angola to test the application.  
  - `Patrice_Lumumba` folder contains  shapefiles of Patrice_Lumumba area in Angola to test the application.  
  - `Sapporo` folder contains  shapefiles of Sapporo area in Japan to test the application.  
- **`wheels>`** folder contains the python wheels to setup on windows environment.  
  - `GDAL-3.4.2-cp37-cp37m-win_amd64.whl` python wheel for the GDAL library.  
  - `rasterio-1.2.10-cp37-cp37m-win_amd64.whl` python wheel for the rasterio library.  
- `.gitignore` contains a list of files and folders to be ignored when commiting to the repository.  
- `authentication.json` contains GEE and GCS credentials to start the application and to upload data to cloud (make sure you add a `private_key.json` file to the repository main folder).  
- `requirements.txt` contains a list of python libraries to be installed on windows environment.  
- `requirements_mac.txt` contains a list of python libraries to be installed on mac environment.

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

`add principals:` allUsers.  
`assigned roles:` storage legacy bucket owner, reader; object owner, reader.  

- In the `authentication.json` file, add the service account, the private key file name and the bucket name.

## Uplaod local 
### maptiles generation
To upload local geotiff files, we have to first produce maptiles.
gdal (`gdal2files`) is used to produce tiles stored in a `<maptiles_folder>` that contains subfolders for different zoom levels.

### upload maptiles
Generated maptiles for this project are hosted in google cloud storage, uploaded using the google-cloud-storage API (API different from earthengine-api, so, authentication process is different but uses the same private-key). After uploading a maptile we can have access to it as layer by using the public url `https://storage.googleapis.com/<bucket_name>/<folder_name>/{z}/{x}/{y}.png`.  
**Note:** Make sure to make your bucket and its objects (folders, files) public and set `owner` permissions for `allUsers` from google cloud storage.

## Usage ([demo video](https://youtu.be/H1e0TWnEqfQ))
### Load area
Global shapefiles (for area to be analised) can be downloaded from [Diva GIS](https://www.diva-gis.org/Data) at different levels and used as input.  
Shapfiles should be uploaded with its corresponding `.dbf, .sbn, .shx, .sbx, .prj` dependencies files at once. Use the data from `test_data` folder to test this application.

### Load Satellite Image
Satellite images ID should follow the format: `LANDSAT/<mission>/<collection>/<tier>/<image_ID>` for landsat and `COPERNICUS/<sentinel_mission>_<optional_processing_level>/<image_ID>` for sentinel. (check image ID availability from [example script](https://code.earthengine.google.com/848200c362694900b6027b30b0e99677) using `ee.ImageCollection`).

#### Example:
`LANDSAT/LC09/C02/T1/LC09_182066_20220611` (use with shapefile Patrice_Lumumba).  
`LANDSAT/LC09/C02/T1/LC09_182068_20220611` (use with shapefile Lobito).  
`LANDSAT/LC09/C02/T1/LC09_108030_20220909` (use with shapefile Sapporo).  
`COPERNICUS/S2_SR/20220805T012659_20220805T013242_T54TWN` (use with shapefile Sapporo).

**Note:** GEE python API only `accepts sampling <= 262144 pixels` (the process of getting pixels from GEE cloud storage). For larger areas you might have to choose a shapefile with a higher level of administrative boundaries of your area of interest (`for example, Sapporo shapefile in` **test_data** `folder`) or divide it into smaller pieces to meet the sampling requirements (`for example, Lobito shapefile in` **test_data** `folder`).

### Get Spectral Index
For spectral index calculator, make sure you understand the satellite image specs (Bands). Only NASA Landsat and ESA Sentinel2 images allowed).

### Image Classification

- **Stack Bands:** list of bands to be stacked for unsupervised classification.  
- **k:** as you wish for the number of clusters.  
- **num_of_subdim (M):**  The  number of subdimensions (from the input nD image) for quantization. Needs to be mltiple of num of bands. The higher the subdimension the slower the algorithm.  
- **Ks:**  represents the maximum digital number. By default it is 256 that corresponds to 8 bits.  
- **sample_size:** The number of pixels you select for quantization.

## Todo
- Clear database. Clear output images from local.
- Check GCS's bucket/object content (spectral indices) and update in database (SpectralIndex table).
- Ask to save output image somewhere else before a new image is classified.
- Fix warning message on put request (currently requires page refresh).
- Explore Atmospheric correction and radiometric calibration for a better classification.
