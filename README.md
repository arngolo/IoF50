# Imagery on the Fly (IoF)
## requirements
python3.7 (create a virtual env with python 3.7)

### windows
pip install requirements.txt (windows)
(Microsoft Build Tolls)[https://www.microsoft.com/en-us/download/details.aspx?id=48159] for pqkmeans.2015 version used in this project. Try a recent version.
### Mac
pip install django
pip install earthengine-api --upgrade
pip install pandas
pip install rasterio
pip install pqkmeans
pip install gdal2tiles
pip install google-cloud-storage
pip install pyproj

### Note:
To upload a shapefile at least `.shp, .dbf, .shx and .prj extension files are required. Select them at once when uploading the vector data.

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
Generated maptiles for this project are hosted in google cloud storage, uploaded using the google-cloud-storage API (API different from earthengine-api, so, authentication process is different but using the same private-key). After uploading a maptile we can have access to it as layer by using the public url `https://storage.googleapis.com/<bucket_name>/<folder_name>/{z}/{x}/{y}.png'`. 
**Note:** Make sure to make your bucket and its objects (folders, files) public and set `owner` permissions for `allUsers` from google cloud storage.
## Usage


