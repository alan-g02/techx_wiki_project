# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
class Backend:

    def __init__(self):
        self.list_page_names = []
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self, bucket_name, blob_name):
        """Write and read a blob from GCS using file-like IO"""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"

        # The ID of your new GCS object
        # blob_name = "storage-object-name"

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        with blob.open("r") as f:
            for name in f:
                self.list_page_names.append(name)  

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

    def get_image(self):
        pass

