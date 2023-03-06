from flask import render_template,send_file,request
from flaskr import backend

backend = backend.Backend()

def make_endpoints(app):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        return render_template('home.html')

    @app.route("/images/<file_name>")
    def images(file_name):
        '''Returns a path/element/src for a file using the get_image method
        
        [IMPORTANT] Only png images supported. Lets try to only upload png images to the bucket.
        [SUGGESTION] Use this in the html <img src="images/{{ file }}"/ alt="Could not find: {{ file }}.">

        Args:
            file_name used to pass the value to get image, and used as a reference in route to support different images.
        '''
        return send_file(backend.get_image(file_name),mimetype='image/png')

    @app.route("/pages")
    def pages():
        return render_template('pages.html')

    @app.route("/logout")
    def logout():
        return render_template('logout.html')
