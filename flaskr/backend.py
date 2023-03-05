# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
from io import BytesIO
from flask import Flask, send_file
from google.cloud.exceptions import NotFound

class Backend:
    def __init__(self):
        self.list_page_names = []
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self, bucket_name, folder_name):
        """Write and read a blob from GCS using file-like IO"""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"

        # The ID of your new GCS object
        # blob_name = "storage-object-name"

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs(folder_name)

        for blob in blobs:
            self.list_page_names.append(blob.name)  

        return self.list_page_names

    def upload(self, bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"
        # The path to your file to upload
        # source_file_name = "local/path/to/file"
        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        return 

    def sign_up(self):
        pass

    def sign_in(self):
        pass

    def get_image(self,file_name):
        '''Returns an image from the ama_wiki_content bucket, in the ama_images folder

        Extracts a blob from the ama_wiki_content bucket that can be used as a route for an image to be rendered in html

        Args:
            file_name: used to complete the path required to find the image blob in the bucket.
        
        '''
        try :
            storage_client = storage.Client()
            bucket = storage_client.bucket('ama_wiki_content')
            blob = bucket.blob('ama_images/' + file_name)
        except:
            return None

        with blob.open("rb") as f:
            return BytesIO(f.read())
        




