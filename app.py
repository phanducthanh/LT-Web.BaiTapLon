import os
import sqlite3
import json
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, login_user, current_user
import services.api_execute
from models.User import User
import db


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Secret key for session
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user_data = db.get_user_by_id(user_id)
    if user_data:
        user = User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
        return user


# Redirect to login page if user is not logged in
@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect('/login')


# Homepage
@app.route('/')
def home_page():
    return 'This is homepage!'


@app.route('/test', strict_slashes=False)
@login_required
def test():
    return "Hi there!"


# Login page
@app.route('/login', methods=["GET", "POST"], strict_slashes=False)
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data = db.get_user(email)
        if user_data:
            user = User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
            if password == user.password:
                login_user(user)
                return "Login success!"
        else:
            return "Wrong username or password!"
    if current_user.is_authenticated:  # check if user is logged in
        return redirect('/')
    return render_template('login.html')


# Sign up page
@app.route('/sign-up', methods=["GET", "POST"], strict_slashes=False)
def sign_up():
    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        try:
            db.add_user(email, username, password)
        except sqlite3.IntegrityError:
            return "Username is exist!"
        return "New user added!"
    return render_template('sign-up.html')


# API to run code
@app.route('/api/execute', methods=["POST"], strict_slashes=False)
def execute():
    data = request.get_json()
    script = data['script']
    stdin = data['stdin']
    language = data['language']
    versionIndex = int(data['versionIndex'])
    result = services.api_execute.compile_code(
        script=script,
        stdin=stdin,
        language=language,
        version=versionIndex
    )
    return json.dumps(result)


@app.route('/idk', strict_slashes=False)
def idk():
    return render_template('idk.html')


if __name__ == '__main__':
    app.run(debug=True)
