# TODO(Project 1): Implement Backend according to the requirements.
import hashlib
from google.cloud import storage
from io import BytesIO
from flask import Flask, send_file
from google.cloud.exceptions import NotFound
import json


class Backend:

    def __init__(self):
        pass

    def get_wiki_page(self, file_name, storage_client=storage.Client()):
        #Implementing bucket/blob
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

    def add_page_to_user_data(self,username,file_name,storage_client=storage.Client(),json_module=json):
        ''' Updates user list of pages authored after uploading a page

        Processes the user json file to a python dictionary, adds the new uploaded page file name to the list.
        Processes the dictionary back to json and uploads.

        Args:
            username: used to update the right user file
            file_name: used to add the file name to the user list of pages authored
            storage_client: used to inject mock storage, uses google storage by default
            json_module: used to inject mock json, uses normal json by default
        '''
        bucket = storage_client.bucket('ama_users_passwords')
        blob = bucket.blob(username)
        user_data = {}
        with blob.open('r') as b:
            user_data = json_module.loads(b.read())
        user_data['pages_uploaded'].append('pages/'+file_name)
        json_data = json_module.dumps(user_data)
        blob.upload_from_string(json_data,content_type="application/json")

    def get_pages_authored(self,username,storage_client=storage.Client(),json_module=json):
        '''Gets the list of pages authored by the user
        
        Converts user data from json to python dictionary and returns key pages_uploaded that contains a list of pages authored

        Args:
            username: used to get the data from the user
            storage_client: used to inject mock storage, uses google storage by default
            json_module: used to inject mock json, uses normal json by default
        '''
        bucket = storage_client.bucket('ama_users_passwords')
        blob = bucket.blob(username)
        user_data = {}
        with blob.open('r') as b:
            user_data = json_module.loads(b.read())
        return user_data['pages_uploaded']
    
    def upload(self, bucket_name, file, file_name, file_type, username, add_page=None):
        """Uploads a file to the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"
        # The path to your file to upload
        # source_file_name = "local/path/to/file"
        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"
        if not add_page:
            add_page = self.add_page_to_user_data

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob('pages/' + file_name)

        blob.upload_from_file(file, content_type=file_type)
        add_page(username,file_name)

    def sign_up(self, username, password, storage_client=storage.Client(), json_module=json):
        #Creating a list of blobs (all_blobs) which holds a file for each username.
        bucket = storage_client.bucket("ama_users_passwords")

        #setting cap for username length
        if len(username) > 32:
            return False

        #Opening list of blobs to read filenames to see if a file matches the username that was just inputted
        blob = bucket.blob(username)
        if blob.exists():
            return False

        else:
            #hashing password and adding it to the username file that correlates with it
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            user_data = {
                "key" : hashed_password,
                "pages_uploaded" : [] 
                }

            json_data = json_module.dumps(user_data)
            blob.upload_from_string(json_data,content_type="application/json")
            return True

    def get_user_key(self, username, storage_client=storage.Client(), json_module=json):
        bucket = storage_client.bucket('ama_users_passwords')
        blob = bucket.blob(username)
        if blob.exists():
            map = {}
            with blob.open('r') as b:
                map = json_module.loads(b.read())
            return map['key']
        else:
            return None

    def sign_in(self,
                username,
                password,
                storage_client=storage.Client(),
                hash=hashlib.sha256,
                get_key=None):
        '''Returns a boolean if the user is found and the password matches.

        Searches the ama_users_passwords bucket for a match with the parameters received.

        Args:
            username: used to search a specific blob in the ama_users_passwords bucket
            password: used to compare to the value inside the username blob
            storage_client: used to receive a mock storage client, default is normal storage client
        '''
        if get_key is None:
            get_key = self.get_user_key
        bucket = storage_client.bucket("ama_users_passwords")
        blob = bucket.blob(username)
        if blob.exists():
            hashed_password = hash(password.encode()).hexdigest()
            key = get_key(username)
            if key == hashed_password:
                return True
            else:
                return False
        else:
            return False

    def get_image(self,
                  file_name,
                  storage_client=storage.Client(),
                  bytes_io=BytesIO):
        '''Returns an image from the ama_wiki_content bucket, in the ama_images folder

        Extracts a blob from the ama_wiki_content bucket that can be used as a route for an image to be rendered in html

        Args:
            file_name: used to complete the path required to find the image blob in the bucket.
            storage_client: used to accept mock storage client, default is normal storage client
            bytes_io: used to accept mock bytes io class, default is normal BytesIO class
                Example class
                    class MockBytes:
                        def __init__(self,data):
                            self.data = data
                        def read(self):
                            return self.data
        '''
        bucket = storage_client.bucket('ama_wiki_content')
        blob = bucket.blob('ama_images/' + file_name)

        if blob.exists():
            with blob.open("rb") as f:
                return bytes_io(f.read())
        else:
            return None
