from google.cloud import storage
import os

# upload maptiles to google cloud storage

def upload_objects_to_gcp(project_directory, bucketName, folderName):
    """Upload files to GCP bucket."""
    os.chdir(project_directory + "/media/output_images")
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucketName)
    for path, subdirs, files in os.walk(folderName):
        for name in files:
            path_local = os.path.join(path, name)
            blob_path = path_local.replace('\\','/')
            blob = bucket.blob(blob_path)
            blob.upload_from_filename(path_local)
    os.chdir(project_directory)