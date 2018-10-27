import os
import json
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
import services.api_execute
from models.User import User
from models.Language import Language
from models.Question import Question
from models.QuestionLevel import QuestionLevel
import db
import mysql.connector


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


@app.route('/language', strict_slashes=False)
@app.route('/language/<language_name>', strict_slashes=False)
@app.route('/language/<language_name>/<question_id>', strict_slashes=False)
def language(language_name=None, question_id=None):
    languages_link = db.get_list_languages()
    if language_name in languages_link:
        questions = []
        if question_id:
            return 'Thanh Dat'
        for question_data in db.get_questions_by_language_name(language_name):
            question = Question(*question_data)
            question.score = db.get_level_by_name(question.level)[2]
            questions.append(question)
        return render_template('language_challenges.html',
                               title=language_name,
                               questions=questions)
    return redirect('/dashboard')


@app.route('/dashboard')
# @login_required
def dashboard():
    languages_data = db.get_languages()  # list of languages data
    languages = []  # save instances of Language
    for language_data in languages_data:
        language = Language(language_data[0], language_data[1], language_data[2])
        languages.append(language)
    return render_template('dashboard.html', languages=languages)


# Homepage
@app.route('/')
def home_page():
    if current_user.is_authenticated:
        return redirect('/dashboard')
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


# Log out
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "<h1>Logged out</h1>"


# Sign up page
@app.route('/sign-up', methods=["GET", "POST"], strict_slashes=False)
def sign_up():
    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        try:
            db.add_user(email, username, password)
        except mysql.connector.errors.IntegrityError:  # duplicate entry
            return "Username or email is exist!"
        return redirect('login')
    if current_user.is_authenticated:
        return redirect('/')
    return render_template('sign-up.html')


# API to run code
@app.route('/api/execute', methods=["POST"], strict_slashes=False)
@login_required
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
