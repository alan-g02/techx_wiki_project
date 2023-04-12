# TODO(Project 1): Implement Backend according to the requirements.
import hashlib
from google.cloud import storage
from io import BytesIO
from flask import Flask, send_file
from google.cloud.exceptions import NotFound
from bs4 import BeautifulSoup
import math


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

    def scan_contents(self,contents,pages_lst=None):
        """Scans contents for references to wiki pages and returns a formatted string.

        Args:
            contents: A string containing the text to scan for wiki page references.
            pages_lst: An optional list of strings representing the names of wiki pages
                to use for the scan. Defaults to None.

        Returns:
            A string containing the original contents with any wiki page references
            formatted as hyperlinks.
        """
        pages_list= pages_lst or self.get_all_page_names('ama_wiki_content','pages/')
        max_length = -math.inf # Length of the longest wiki page title
        pages_set = set() # Set of strings with the list of pages in the string
        for i in range(len(pages_list)):
            temp = pages_list[i][6:]
            if len(temp) > max_length:
                max_length = len(temp)
            pages_set.add(temp)
        used_pages = set() # Saves the pages that have already been used in the
        split_contents = contents.split()
        result = ''       
        i = 0
        while i < len(split_contents):
            longest_valid_title = ''
            temp = ''
            skip_count = 0
            j = i
            while (j < len(split_contents)) and (len(temp) <= max_length):
                if temp == '':
                    temp += split_contents[j]
                else:
                    temp += ' ' + split_contents[j]   
                dot_at_the_end = False   
                if temp[-1] == '.': # Deleting "." because words might be at the end of a sentence
                    temp = temp[:-1]      
                    dot_at_the_end = True  
                if (temp in pages_set) and (temp not in used_pages) and (len(temp) > len(longest_valid_title)):
                    longest_valid_title = temp
                    if dot_at_the_end: # Adds the "." back, Why? To remember later there is a dot and include it in the final string
                        longest_valid_title += '.'
                    skip_count = j-i
                j += 1
            if longest_valid_title == '':
                if result == '':
                    result += split_contents[i]
                else:
                    result += ' ' + split_contents[i]
            else:
                dot_at_the_end_part_2 = False
                if longest_valid_title[-1] == '.': # Removes the dot
                    longest_valid_title = longest_valid_title[:-1]
                    dot_at_the_end_part_2 = True
                used_pages.add(longest_valid_title)
                longest_valid_title = f'<a href=\"/page_results?current_page=pages/{longest_valid_title}\">{longest_valid_title}</a>' # Creates a hyperlink of the linked page
                if dot_at_the_end_part_2: # Adds the dot after the hyperlink if there was a dot
                    longest_valid_title += '.'
                if result == '':
                    result += longest_valid_title
                else:
                    result += ' ' + longest_valid_title
            i += skip_count + 1
        return result

    def upload(self, bucket_name, file, file_name, file_type, storage_client=storage.Client(), soup=BeautifulSoup, scan=None):
        """ Uploads a file to the bucket.

        The contents of the incoming file are cleaned up of any unwanted html blocks, then another function in the backend class is called
        to create hyperlinks for related pages in the wiki. Finally the formatted content is uploaded into the bucket.

        Args:
            file: The file object to upload.
            file_name: The name to give the uploaded file.
            file_type: The content type of the uploaded file.
            storage_client: used to accept mock storage client, default is normal storage client
            soup: used to accept mock soup, default uses BeautifulSoup()
            mock_format: used to replace self.format() to remove dependecy
        """
        # Checks if any mock objects were injected
        if scan is None:
            scan = self.scan_contents
            
        # Read the contents fo the file into a byte string
        file_contents = file.read()

        # Sanitze any HTML tags in the file contents
        clean_content = soup(file_contents,'html.parser',from_encoding='utf-8').get_text()

        # [ALERT] NEED TO ADD CALL TO FORMATTING AFTER MERGE REQUEST IS APPROVED
        # CURRENTLY IT JUST UPLOADS A CLEAN STRING AFTER DELETED ANY HTML
        formatted_content = scan(clean_content)

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob('pages/' + file_name)
        blob.upload_from_string(formatted_content, content_type=file_type)
        return formatted_content


    def sign_up(self, username, password, storage_client=storage.Client()):
        #Creating a list of blobs (all_blobs) which holds a file for each username.
        bucket = storage_client.bucket("ama_users_passwords")

        #setting cap for username length
        if len(username) > 32:
            print('username too long')
            return False

        #Opening list of blobs to read filenames to see if a file matches the username that was just inputted
        blob = bucket.blob(username)
        if blob.exists():
            print('username already exists')
            return False

        else:
            #hashing password and adding it to the username file that correlates with it
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            blob.upload_from_string(hashed_password)
            print('user created successfully')
            return True

    def sign_in(self,
                username,
                password,
                storage_client=storage.Client(),
                hash=hashlib.sha256):
        '''Returns a boolean if the user is found and the password matches.

        Searches the ama_users_passwords bucket for a match with the parameters received.

        Args:
            username: used to search a specific blob in the ama_users_passwords bucket
            password: used to compare to the value inside the username blob
            storage_client: used to receive a mock storage client, default is normal storage client
        '''
        bucket = storage_client.bucket("ama_users_passwords")
        blob = bucket.blob(username)
        if blob.exists():
            hashed_password = hash(password.encode()).hexdigest()
            with blob.open("r") as f:
                if f.read() == hashed_password:
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
