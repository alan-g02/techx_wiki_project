from flaskr.backend import Backend
from unittest.mock import MagicMock,patch
import unittest

mock_client = MagicMock()
bucket = MagicMock()
blob = MagicMock()
backend = Backend()



@patch("google.cloud.storage.Client")
def test_upload(mock_storage):
    mock_storage.return_value = mock_client

    mock_client.bucket.return_value = bucket

    bucket.blob.return_value = blob    

    backend = Backend()
    
    backend.upload("wiki", "desktop","gcb")
    mock_client.bucket.assert_called_with("wiki") #if error check the test names for buckets
    bucket.blob.assert_called_with("gcb") 

    blob.upload_from_filename.assert_called_with("desktop")


@patch("google.cloud.storage.Client")
def test_get_all_page_names(mock_storage):
    mock_storage.return_value = mock_client

    mock_client.bucket.return_value = bucket

    bucket.blob.return_value = blob    

    backend.get_all_page_names("wiki", "pages")
    mock_client.bucket.assert_called_with("wiki")
    bucket.blob.assert_called_with("pages")

@patch("google.cloud.storage.Client")
def test_sign_up(self, mock_storage):
    mock_storage.return_value = mock_client #creating a mock to return client
    mock_client.bucket.return_value = bucket #creating a mock to return bucket
    bucket.blob.return_value = blob #creating mock to return blob

    backend.sign_up("username", "password") #calling the sign in function from back end taking in "username" for the username and "password" for the password
    mock_client.bucket.assert_called_with("ama_users_passwords") #Checks to see if it's able to store mocked username/hashed password into the bucket

    
@patch("google.cloud.storage.Client")
def test_sign_up_username_length(self, mock_storage):
    mock_storage.return_value = mock_client
    mock_client.bucket.return_value = bucket
    bucket.blob.return_value = blob

    #assertion to check if the function for username being too long works
    with self.asserRaises: 
        backend.sign_up("IAMASUPERLONGUSERNAMEANDIAMHUNGRYRIGHTNOW", "password")

@patch("google.cloud.storage.Client")
def test_sign_up_is_member(self, mock_storage):
    mock_storage.return_value = mock_client
    mock_client.bucket.return_value = bucket
    bucket.blob.return_value = blob
    blob.exists.return_value = True #Tells blob that it exists already

    #assertion to check the function of a username already being in use 
    with self.asserRaises:
        backend.sign_up("username", "password")

@patch("google.cloud.storage.Client")
def test_get_wiki_page(mock_storage):
    mock_storage.return_value = mock_client
    mock_client.bucket.return_value = bucket
    bucket.blob.return_value = blob

    #testing mock to see if it's able to grab the wiki page.
    backend.get_wiki_page() #what do I do inside of this call???

    
