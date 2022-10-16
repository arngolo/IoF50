# requirements
python3.7 (create a virtual env with python 3.7)

# windows
pip install requirements.txt (windows)
(Microsoft Build Tolls)[https://www.microsoft.com/en-us/download/details.aspx?id=48159] for pqkmeans.2015 version used in this project. Try a recent version.
# Mac
pip install django
pip install earthengine-api --upgrade
pip install pandas
pip install rasterio
pip install pqkmeans

### to store numpy arrays in the database
pip install django-ndarrayfield

# Note:
We can upload a shapefile to GEE in the assets section (under users/username location).
at least `.shp, .dbf, .shx and .prj extension files are required. 

# GEE python authentication

Create a service account (first create a google cloud project from the developer IDE (assets section)).

On the project name click the home button, select the cloud console menu > `IAM & admins` > service accounts > `create service account`.

Create and download a JSON private key file for the service account.

## To authenticate:
- Place the private key in the root location of this project.
- In the `authentication.json` file, add the service account and the private key file name.


