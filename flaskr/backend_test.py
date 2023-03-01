import pytest
from flaskr.backend import Backend
from unittest.mock import MagicMock,patch
# TODO(Project 1): Write tests for Backend methods.

@patch("google.cloud.storage.Client")
def test_upload(mock_storage):
    mock_client = MagicMock()
    mock_storage.return_value = mock_client

    bucket = MagicMock()
    mock_client.bucket.return_value = bucket

    blob = MagicMock()
    bucket.blob.return_value = blob    

    backend = Backend()
    backend.upload("wiki", "desktop","gcb")
    mock_client.bucket.assert_called_with("wiki")
    bucket.blob.assert_called_with("gcb")

    blob.upload_from_filename.assert_called_with("desktop")


@patch("google.cloud.storage.Client")
def test_get_all_page_names(mock_storage):
    mock_client = MagicMock()
    mock_storage.return_value = mock_client

    bucket = MagicMock()
    mock_client.bucket.return_value = bucket

    blob = MagicMock()
    bucket.blob.return_value = blob    

    backend = Backend()
    backend.get_all_page_names("wiki", "pages")
    
    mock_client.bucket.assert_called_with("wiki")
    bucket.blob.assert_called_with("pages")