from flaskr.backend import Backend
from unittest.mock import MagicMock,patch
from unittest.mock import patch, mock_open
from unittest import mock

import pytest

class test_list_blobs:
    def __init__(self,name):
        self.name = name

mock_client = MagicMock()
bucket = MagicMock()
blob = MagicMock()
backend = Backend()
file = MagicMock()


@patch("google.cloud.storage.Client")
def test_upload(mock_storage):
    mock_storage.return_value = mock_client
    mock_client.bucket.return_value = bucket
    bucket.blob.return_value = blob  

    backend.upload("wiki","test_file","page",".txt")
    mock_client.bucket.assert_called_with("wiki")
    bucket.blob.assert_called_with("pages/page")
    blob.upload_from_file.assert_called_with("test_file",content_type=".txt")


@patch("google.cloud.storage.Client")
def test_get_all_page_names(mock_storage):
    mock_storage.return_value = mock_client
    mock_client.bucket.return_value = bucket   

    backend.get_all_page_names("wiki", "pages")
    mock_client.bucket.assert_called_with("wiki")
    bucket.list_blobs.assert_called_with(prefix="pages")

@patch("google.cloud.storage.Client")
def test_get_all_page_nameslist(mock_storage):
    mock_storage.return_value = mock_client
    mock_client.bucket.return_value = bucket
    test_page1 = test_list_blobs("pages/")
    test_page2 = test_list_blobs("pages/page")
    bucket.list_blobs.return_value = [test_page1,test_page2]

    pagenames = backend.get_all_page_names("wiki", "pages")
    assert pagenames == ["pages/page"]    

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
def test_get_wiki_page(self,mock_storage):
    mock_storage.return_value = mock_client
    mock_client.bucket.return_value = bucket
    blob = bucket.blob("/pages/file_name" )
    file_content = "I am inside file"
    mock_open = mock.mock_open(read_data = file_content)

    blob.upload_from_file(mock_open)   #Upleoads blob to bucket

    with self.asserRaises:
       backend.get_wiki_page("file_name")

@patch("google.cloud.storage.Client")
def test_get_image_succeeds(mock_storage):
    ''' Tests get_image() and expects a successful retrival

    Tests get_image() and expects a successful retrival.
    Removes dependencies: storage client, bucket, blob, and bytesio

    '''
    class MockBytes:
        '''Mocks the class of BytesIO

        Mocks the class of BytesIO with similar needed methods.

        Attributes:
            data: saves data when initializing the object
        '''
        def __init__(self,data):
            self.data = data
        def read(self):
            '''
            Returns the attribute data in the class
            '''
            return self.data

    # Creates Magic Mocks
    my_client = MagicMock()
    my_bucket = MagicMock()
    my_blob = MagicMock()

    backend = Backend()

    # Establishes return values for mock operations
    mock_storage = my_client
    my_client.bucket.return_value = my_bucket
    my_bucket.blob.return_value = my_blob
    my_blob.exists.return_value = True # Makes the function believe that the blob exists

    # Creates a mock image with binary data
    my_image_data = b"This is an image"

    # Sets blob open value of read to mock image
    my_blob.open = mock_open(read_data=my_image_data)

    # Returns a bytesio object, in this case, the mock bytes io object.
    results = backend.get_image('my_image_name',
                                mock_storage,
                                MockBytes)

    # Calls the method read() inside the mock bytesio object returned from get_image()
    assert results.read() == my_image_data 

@patch("google.cloud.storage.Client")
def test_get_image_fail(mock_storage):
    ''' Tests get_image() and expects a successful retrival

    Tests get_image() and expects a successful retrival.
    Removes dependencies: storage client, bucket, blob, and bytesio

    '''
    class MockBytes:
        '''Mocks the class of BytesIO

        Mocks the class of BytesIO with similar needed methods.

        Attributes:
            data: saves data when initializing the object
        '''
        def __init__(self,data):
            self.data = data
        def read(self):
            '''
            Returns the attribute data in the class
            '''
            return self.data

    # Creates Magic Mocks
    my_client = MagicMock()
    my_bucket = MagicMock()
    my_blob = MagicMock()

    backend = Backend()

    # Establishes return values for mock operations
    mock_storage = my_client
    my_client.bucket.return_value = my_bucket
    my_bucket.blob.return_value = my_blob
    my_blob.exists.return_value = False # Makes the function believe that the blob does not exist

    # Creates a mock image with binary data
    my_image_data = b"This is an image"

    # Sets blob open value of read to mock image
    my_blob.open = mock_open(read_data=my_image_data)

    # Returns a bytesio object, in this case, the mock bytes io object.
    results = backend.get_image('my_image_name',
                                mock_storage,
                                MockBytes)

    # Since the blob does not exist, it returns None
    assert results == None
    
    
    