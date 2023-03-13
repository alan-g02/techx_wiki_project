import flask
import flask_login
from flask_login import UserMixin, LoginManager
from flask import render_template, request, redirect, url_for
from flaskr import backend

backend = backend.Backend()

class User(UserMixin):
    pass
        
def make_endpoints(app,login_manager):
    @login_manager.user_loader
    def user_loader(username):
        user = User()
        user.id = username
        return user

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            # Get the form data
            username = request.form['username']
            password = request.form['password']

            #still waiting on signup in backend
            if backend.sign_up(username,password):
                user = User()
                user.id = username
                flask_login.login_user(user)
                return redirect(url_for('home'))
            else:
                return render_template('signup.html',status="used")
        return render_template('signup.html')

    @app.route("/login", methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            # Get the form data
            username = request.form['username']
            password = request.form['password']

            #still waiting on signup in backend
            if backend.sign_in(username,password): # Checks if the username and password are correct
                user = User()
                user.id = username
                flask_login.login_user(user)
                return render_template('login.html', status= "is_member")
            return render_template('login.html', status= "not_member")
        return render_template('login.html')


