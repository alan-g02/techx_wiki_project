# TODO(Project 1): Implement Backend according to the requirements.
import hashlib
from google.cloud import storage
from io import BytesIO
from flask import Flask, send_file
from google.cloud.exceptions import NotFound

class Backend:
    def __init__(self):
        pass
        
    def get_wiki_page(self, file_name):
        #Implimenting client/bucket/blob
        storage_client = storage.Client()
        bucket_wikiPage = storage_client.bucket("ama_wiki_content")
        blob = bucket_wikiPage.blob(file_name)

        #opening/reading blob as a file and returning the file inside of it.
        with blob.open('r') as f:
            return f.read()


    def get_all_page_names(self, bucket_name, folder_name):
        """Write and read a blob from GCS using file-like IO"""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"

        # The ID of your new GCS object
        # blob_name = "storage-object-name"
        list_page_names = []
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=folder_name)
        
        for blob in blobs:
            if not blob.name.endswith('/'):
               list_page_names.append(blob.name)  

        return list_page_names

    def upload(self, bucket_name, file, file_name,file_type):
        """Uploads a file to the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"
        # The path to your file to upload
        # source_file_name = "local/path/to/file"
        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob('pages/' + file_name)

        blob.upload_from_file(file,content_type=file_type)
        return 

    def sign_up(self, username, password):
        #Creating list of blobs (all_blobs) which holds a file for each username.
        storage_client = storage.Client()
        bucket = storage_client.bucket("ama_users_passwords")
       
        #setting cap for username length
        if len(username) > 32:
            raise Exception('Must be less than 33 characters')


        #Opening list of blobs to read filenames to see if a file matches the username that was just inputted              
        blob = bucket.blob(username)
        if blob.exists():
            raise Exception("Username is already taken")


        else:
        #hashing password and adding it to the username file that correlates with it
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            blob.upload_from_string(hashed_password)


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
        




