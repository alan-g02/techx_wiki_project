from flaskr.backend import Backend
from unittest.mock import MagicMock,patch
import pytest

class test_list_blobs:
    def __init__(self,name):
        self.name = name

mock_client = MagicMock()
bucket = MagicMock()
blob = MagicMock()
backend = Backend()

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

