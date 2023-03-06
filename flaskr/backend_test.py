from flaskr.backend import Backend
from unittest.mock import MagicMock,patch

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
    mock_client.bucket.assert_called_with("wiki")
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