# requirements
python3.7 (create a virtual env with python 3.7)

# windows
pip install requirements.txt (windows)
# Mac
pip install pillow
pip install earthengine-api --upgrade
pip install pandas
pip install geopandas
pip install rasterio
pip install pqkmeans
pip install pillow

### to store numpy arrays in the database
pip install django-ndarrayfield

# Note:
We can upload a shapefile to GEE in the assets section (under users/username location).
at least `.shp, .dbf, .shx and .prj extension files are required. 

# GEE python authentication

Create a service account (first create a google cloud project from the developer IDE (assets section)).

On the project name click the home button, select the cloud console menu > `IAM & admins` > service accounts > `create service account`.

# Note: 
Service account name: cs50w-arngolo
Service account ID: cs50w-arngolo
Service account email: cs50w-arngolo@arngolo.iam.gserviceaccount.com

Create and download a JSON private key file for the service account.
