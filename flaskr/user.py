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

    # @app.route("/login", methods = ['GET', 'POST'])
    # def login():
    #     # username = request.form['username'] #requesting username
    #     # password = request.form['password'] #requesting password
    #     # is_member = backend.sign_in(username,password) #making is_member variable that takes the grabbed username, password from the backend.


    #     #Checks to see if the username and password are in the blob and returns the specific login function from html
    #     # if is_member:
    #     #If person logging in is a member
    #     return render_template('login.html', status = 'is_member')


    #     #Checks to see if the username and password are not in the blob and returns the specific login function from html
    #     # else:
    #     #If Person logging in isn't a member
    #         # return render_template('login.html', status = 'not_member')

    @app.route("/login", methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            # Get the form data
            username = request.form['username']
            password = request.form['password']

            #still waiting on signup in backend
            if backend.sign_in(username,password,redirect): # Checks if the username and password are correct
                user = User()
                user.id = username
                redirect = True
                flask_login.login_user(user)
                return render_template('login.html', status= "is_member")
            return render_template('login.html', status= "not_member")
        return render_template('login.html')


