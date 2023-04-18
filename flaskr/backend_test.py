from flaskr.backend import Backend
from unittest.mock import MagicMock, patch
from unittest.mock import patch, mock_open
from unittest import mock

import pytest


class test_list_blobs:

    def __init__(self, name):
        self.name = name


mock_client = MagicMock()
bucket = MagicMock()
blob = MagicMock()
backend = Backend()
file = MagicMock()

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
    bucket.list_blobs.return_value = [test_page1, test_page2]

    pagenames = backend.get_all_page_names("wiki", "pages")
    assert pagenames == ["pages/page"]


@patch("google.cloud.storage.Client")
def test_sign_up_success(mock_storage):
    # Path: Username does not exist, created sucessfully
    # Creates Magic Mocks
    my_bucket = MagicMock()
    my_blob = MagicMock()
    mock_json = MagicMock()

    backend = Backend()

    mock_storage.bucket.return_value = my_bucket
    my_bucket.blob.return_value = my_blob
    my_blob.exists.return_value = False  # Makes the function believe that the blob does not exist
    mock_json.dumps.return_value = 'This is a json file'

    results = backend.sign_up('username', 'password', mock_storage, mock_json)
    mock_storage.bucket.assert_called_with('ama_users_passwords')
    my_bucket.blob.assert_called_with('username')
    my_blob.upload_from_string.assert_called_with('This is a json file',content_type='application/json')
    assert results == True


@patch("google.cloud.storage.Client")
def test_sign_up_username_length(mock_storage):
    # Path: Username is too long, sign up unsucessful
    my_bucket = MagicMock()
    my_blob = MagicMock()

    mock_storage.bucket.return_value = my_bucket
    my_bucket.blob.return_value = my_blob

    assert backend.sign_up(
        "usernameistoolong123456789123456789123456789123456789",
        "passworddoesntmatter", mock_storage) == False


@patch("google.cloud.storage.Client")
def test_sign_up_is_member(mock_storage):
    # Path: User already exists
    my_bucket = MagicMock()
    my_blob = MagicMock()

    mock_storage.bucket.return_value = my_bucket
    my_bucket.blob.return_value = blob
    my_blob.exists.return_value = True  # Forces the return value of exists() to be true, for path purposes

    assert backend.sign_up("useralreadyexists", "passworddoesntmatter",
                           mock_storage) == False


@patch("google.cloud.storage.Client")
def test_get_wiki_page(mock_storage):
    my_client = MagicMock()
    my_bucket = MagicMock()
    my_blob = MagicMock()
    backend = Backend()

    mock_storage = my_client
    my_client.bucket.return_value = my_bucket
    my_bucket.blob.return_value = my_blob

    my_image_data = "Contents of the file"
    my_blob.open = mock_open(read_data=my_image_data)

    results = backend.get_wiki_page('my_image_name', mock_storage)
    assert results == "Contents of the file"


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

        def __init__(self, data):
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
    my_blob.exists.return_value = True  # Makes the function believe that the blob exists

    # Creates a mock image with binary data
    my_image_data = b"This is an image"

    # Sets blob open value of read to mock image
    my_blob.open = mock_open(read_data=my_image_data)

    # Returns a bytesio object, in this case, the mock bytes io object.
    results = backend.get_image('my_image_name', mock_storage, MockBytes)

    # Calls the method read() inside the mock bytesio object returned from get_image()
    assert results.read() == my_image_data


@patch("google.cloud.storage.Client")
def test_get_image_fail(mock_storage):
    ''' Tests get_image() and expects a successful retrival

    Tests get_image() and expects a successful retrival.
    Removes dependencies: storage client, bucket, blob, and bytesio

    '''

    class MockBytes:
        '''Mocks the class of BytesIO with similar needed methods.

        Attributes:
            data: saves data when initializing the object
        '''

        def __init__(self, data):
            self.data = data

        def read(self):
            # Returns the attribute data in the class
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
    my_blob.exists.return_value = False  # Makes the function believe that the blob does not exist

    # Creates a mock image with binary data
    my_image_data = b"This is an image"

    # Sets blob open value of read to mock image
    my_blob.open = mock_open(read_data=my_image_data)

    # Returns a bytesio object, in this case, the mock bytes io object.
    results = backend.get_image('my_image_name', mock_storage, MockBytes)

    # Since the blob does not exist, it returns None
    assert results == None


@patch("google.cloud.storage.Client")
def test_sign_in_found_match(mock_storage):
    '''Tests sign in(), expects to find user and the password matches

    Assumes the blob exists, open returns the password in a string.
    Path: User blob exists, password in blob and password match.
    Removes dependencies: storage client, bucket, blob, and hashlib
    '''

    class Hash:
        '''Mocks the hashlib.sha256 class with similar needed methods.

        Attributes:
            data: used to store a string
        '''

        def __init__(self, data):
            self.data = data.decode()

        def hexdigest(self):
            return self.data

    def mock_get_user_key(username):
        return 'password'

    # Creates Magic Mocks
    my_bucket = MagicMock()
    my_blob = MagicMock()

    backend = Backend()

    # Establishes return values for mock operations
    mock_storage.bucket.return_value = my_bucket
    my_bucket.blob.return_value = my_blob
    my_blob.exists.return_value = True  # Makes the function believe that the blob exists

    result = backend.sign_in("user123", "password", mock_storage, Hash, mock_get_user_key)
    mock_storage.bucket.assert_called_with('ama_users_passwords')
    my_bucket.blob.assert_called_with('user123')
    assert result == True


@patch("google.cloud.storage.Client")
def test_sign_in_found_nomatch(mock_storage):
    '''Tests sign in(), expects to find user and the password does not match

    Assumes the blob exists, open returns the password in a string.
    Path: User blob exists, password in blob and password do not match.
    Removes dependencies: storage client, bucket, blob, and hashlib
    '''

    class Hash:
        '''Mocks the hashlib.sha256 class with similar needed methods.

        Attributes:
            data: used to store a string
        '''

        def __init__(self, data):
            self.data = data.decode()

        def hexdigest(self):
            return self.data

    def mock_get_user_key(username):
        return 'password'

    # Creates Magic Mocks
    my_bucket = MagicMock()
    my_blob = MagicMock()

    backend = Backend()

    # Establishes return values for mock operations
    mock_storage.bucket.return_value = my_bucket
    my_bucket.blob.return_value = my_blob
    my_blob.exists.return_value = True  # Makes the function believe that the blob exists

    result = backend.sign_in("user123", "pass321", mock_storage, Hash, mock_get_user_key)
    mock_storage.bucket.assert_called_with('ama_users_passwords')
    my_bucket.blob.assert_called_with('user123')
    assert result == False


@patch("google.cloud.storage.Client")
def test_sign_in_not_found(mock_storage):
    '''Tests sign in(), does not find the user.

    Assumes the blob exists, open returns the password in a string.
    Path: User does not exist.
    Does not matter if password and and input match, user does not exist.
    Removes dependencies: storage client, bucket, blob, and hashlib
    '''

    class Hash:
        '''Mocks the hashlib.sha256 class with similar needed methods.

        Attributes:
            data: used to store a string
        '''

        def __init__(self, data):
            self.data = data.decode()

        def hexdigest(self):
            return self.data

    # Creates Magic Mocks
    my_bucket = MagicMock()
    my_blob = MagicMock()

    backend = Backend()

    # Establishes return values for mock operations
    mock_storage.bucket.return_value = my_bucket
    my_bucket.blob.return_value = my_blob
    my_blob.exists.return_value = False  # Makes the function believe that the blob does not exist

    result = backend.sign_in("user123", "password123", mock_storage, Hash)
    mock_storage.bucket.assert_called_with('ama_users_passwords')
    my_bucket.blob.assert_called_with('user123')
    assert result == False

@patch("google.cloud.storage.Client")
def test_upload(mock_storage):
    ''' Tests upload method in the backend class
    
    Asserts if the methods are called with the appropiate parameters, and also if the right content was uploaded.
    '''
    class Soup:
        ''' Used to mock BeautifulSoup()

        Mocks BeautifulSoup() to remove a dependency. Using the same amount of parameters and storing them in dummy attributes.
        '''
        def __init__(self,contents,parser_type,from_encoding):
            self.contents = contents
            self.parser_type = parser_type
            self.encoding = from_encoding
        def get_text(self):
            '''Returns a string of the contents without html blocks'''
            return 'This is the contents of the uploaded file with '

    def mock_format(content):
        'Returns a string of the formatted string, which is really the same as what mock soup returns'
        return 'This is the contents of the uploaded file with '

    def mock_add_page(username,filename):
        return 1

    # Creates Magic Mocks
    my_bucket = MagicMock()
    my_blob = MagicMock()
    mock_file = MagicMock()

    # Establishes return values for mock operations
    mock_storage.bucket.return_value = my_bucket
    my_bucket.blob.return_value = my_blob
    mock_file.read.return_value = b'This is the contents of the uploaded file with <Illegal html>'

    # Calls the function being tested
    backend = Backend()
    result = backend.upload("my_bucket", mock_file, "test_file", "text/html", "user123", mock_storage,Soup,mock_format,mock_add_page)

    mock_file.read.assert_called_once()
    mock_storage.bucket.assert_called_with("my_bucket")
    my_bucket.blob.assert_called_with('pages/test_file')
    my_blob.upload_from_string.assert_called_with('This is the contents of the uploaded file with ', content_type="text/html")
    assert result == 'This is the contents of the uploaded file with '

def test_scan_contents():
    ''' Tests the functionality of the scan_contents method.'''
    # Input values
    contents = 'This is a reference to Page 1. This is not a reference to Page 1. This is a reference to Page 2. This is not a reference page 3.'
    pages = ['pages/Page 1', 'pages/Page 2','pages/Page 3']
    backend = Backend()

    result = backend.scan_contents(contents,pages)

    assert result == 'This is a reference to <a href="/page_results?current_page=pages/Page 1\">Page 1</a>. This is not a reference to Page 1. This is a reference to <a href="/page_results?current_page=pages/Page 2\">Page 2</a>. This is not a reference page 3.'


    
@patch('google.cloud.storage.Client')
def test_get_user_key_success(mock_storage):
    ''' Tests get_user_key(), the blob is found

    Expects to return the password of the user after processing the json information
    Removes google storage and json dependency
    '''
    # Creates magic mocks
    my_bucket = MagicMock()
    my_blob = MagicMock()
    mock_json = MagicMock()

    backend = Backend()

    # Sets return values for important functions that need dependencies
    mock_storage.bucket.return_value = my_bucket
    my_bucket.blob.return_value = my_blob
    my_blob.exists.return_value = True
    mock_json.loads.return_value = {'key':'pass123456'}
    my_blob.open = mock_open(read_data="This is a json file content")

    # Asserts output of the method and method calls with specific parameters
    result = backend.get_user_key('user123',mock_storage,mock_json)
    mock_storage.bucket.assert_called_with('ama_users_passwords')
    my_bucket.blob.assert_called_with('user123')
    assert result == 'pass123456'

@patch('google.cloud.storage.Client')
def test_get_user_key_fail(mock_storage):
    ''' Tests get_user_key(), the blob is found

    Expects to return the password of the user after processing the json information
    Removes google storage and json dependency
    '''
    # Creates magic mocks
    my_bucket = MagicMock()
    my_blob = MagicMock()

    backend = Backend()

    # Sets return values for important functions that need dependencies
    mock_storage.bucket.return_value = my_bucket
    my_bucket.blob.return_value = my_blob
    my_blob.exists.return_value = False

    # Asserts output of the method and method calls with specific parameters
    result = backend.get_user_key('user123',mock_storage)
    mock_storage.bucket.assert_called_with('ama_users_passwords')
    my_bucket.blob.assert_called_with('user123')
    assert result == None

@patch('google.cloud.storage.Client')
def test_add_page_to_user_data(mock_storage):
    ''' Tests add_page_to_user_data'''
    def mock_dumps(input_map):
        '''Returns a string a map'''
        result = '{'
        for key in input_map.keys():
            result += key + ':' + ''.join(input_map[key]) + ','
        result = result[:-1] + '}'
        return result

    # Create magic mocks
    my_bucket = MagicMock()
    my_blob = MagicMock()
    mock_json = MagicMock()

    backend = Backend()

    # Set return values for important functions
    mock_storage.bucket.return_value = my_bucket
    my_bucket.blob.return_value = my_blob
    my_blob.open = mock_open(read_data="User data")
    mock_json.loads.return_value = { 'password':'hello1234' , 'pages_uploaded': [] }
    mock_json.dumps = mock_dumps

    # Assert if methods are called with specific parameters
    backend.add_page_to_user_data('user123','my_file',mock_storage,mock_json)
    mock_storage.bucket.assert_called_with('ama_users_passwords')
    my_bucket.blob.assert_called_with('user123')
    my_blob.upload_from_string.assert_called_with('{password:hello1234,pages_uploaded:pages/my_file}',content_type='application/json')

@patch('google.cloud.storage.Client')
def test_get_pages_authored(mock_storage):
    ''' Tests get_pages_authored() '''
    # Create magic mocks
    my_bucket = MagicMock()
    my_blob = MagicMock()
    mock_json = MagicMock()

    backend = Backend()

    # Set return values for important functions
    mock_storage.bucket.return_value = my_bucket
    my_bucket.blob.return_value = my_blob
    my_blob.open = mock_open(read_data="User data")
    mock_json.loads.return_value = { 'password':'hello1234' , 'pages_uploaded': ['pages/my_file'] }

    # Assert if methods are called with specific parameters
    assert ['pages/my_file'] == backend.get_pages_authored('user1234',mock_storage,mock_json)
    mock_storage.bucket.assert_called_with('ama_users_passwords')
    my_bucket.blob.assert_called_with('user1234')





