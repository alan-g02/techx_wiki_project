from flask import render_template, send_file, request, redirect, url_for
from flaskr import backend
from flask_login import logout_user, current_user

backend = backend.Backend()


def make_endpoints(app):

    @app.route("/")
    def home():
        return render_template('home.html')

    @app.route("/about")
    def about():
        return render_template('about.html')

    @app.route('/upload')
    def upload():
        return render_template('upload.html')

    @app.route("/pages")
    def pages():
        pages = backend.get_all_page_names("ama_wiki_content", "pages/")
        return render_template('pages.html', pagenames=pages)

    @app.route("/page_results")
    def page_results():
        current_page = request.args.get('current_page')
        contents = backend.get_wiki_page(current_page)
        return render_template('page_results.html',
                               pagename=current_page[6:],
                               contents=contents)

    @app.route("/logout")
    def logout():
        logout_user()
        return render_template('logout.html')

    @app.route("/images/<file_name>")
    def images(file_name):
        '''Returns a path/element/src for a file using the get_image method
        
        [IMPORTANT] Only png images supported. Lets try to only upload png images to the bucket.
        [SUGGESTION] Use this in the html <img src="images/{{ file }}"/ alt="Could not find: {{ file }}.">

        Args:
            file_name used to pass the value to get image, and used as a reference in route to support different images.
        '''
        return send_file(backend.get_image(file_name), mimetype='image/png')

    @app.route('/upload_wiki', methods=['POST'])
    def handle_upload():
        '''Handles the form block in upload.html

        A route to handle file uploads from upload.html, using POST request. Makes sure there are no empty values.

        [DEPENDENCIES] upload(), get_all_page_names(), and "request".
        
        Variables:
            input_value: Stores the value inside the input block named 'wikiname'. Empty value error handled.
            file: Stores the value in input block named 'file_to_upload'. Empty field (no file uploaded yet) handled.
            pages: Stores the list of pages in the bucket 'ama_wiki_content'

        '''
        input_value = request.form['wikiname']
        file = request.files.get('file_to_upload')
        pages = backend.get_all_page_names('ama_wiki_content', 'blob')
        if input_value in pages:
            # Wiki name already in use
            return render_template('upload.html', status='used')
        elif 'file_to_upload' not in request.files:
            return render_template('upload.html', status='no_file')
        elif input_value.strip() == '':
            # Input is empty
            return render_template('upload.html', status='empty')
        elif file.content_type != 'text/plain':
            # If not .txt
            return render_template('upload.html', status='wrong_file')
        else:
            backend.upload('ama_wiki_content', file, input_value, 'text/plain', current_user.id,True)
            return render_template('upload.html', status='successful')
