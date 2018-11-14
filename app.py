import os
import json
from copy import deepcopy
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
import services.api_execute
from models.User import User
from models.Language import Language
from models.Question import Question
from models.QuestionLevel import QuestionLevel
from models.UserQuestion import UserQuestion
import db
import mysql.connector


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Secret key for session
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """
    Login user
    :param user_id:
    :return: user
    """
    user_data = db.get_user_by_id(user_id)
    if user_data:
        user = User(*user_data)
        return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    """
    Redirect to login page if guest access the page that requires login
    :return: login page
    """
    return redirect('/login')


@app.route('/language', strict_slashes=False)
@app.route('/language/<language_name>', strict_slashes=False)
@app.route('/language/<language_name>/<int:question_id>', strict_slashes=False)
@login_required
def language(language_name=None, question_id=None):
    languages_link = db.get_list_languages()  # get all languages name in DB to check url
    if language_name in languages_link:  # if url is valid
        questions = []
        for question_data in db.get_questions_by_language_name(language_name):
            question = Question(*question_data[0:7])
            question.question_level = question_data[8]
            question.question_language = question_data[11]
            question.question_score = question_data[9]
            questions.append(question)
        if question_id:  # url for question
            for question in questions:
                if question_id == question.question_id:
                    get_user_question = db.get_userquestion(int(current_user.get_id()), question_id)
                    test_submit = None
                    if get_user_question:
                        userquestion = UserQuestion(*get_user_question)
                        test_submit = userquestion.test_submit
                    return render_template('challenge.html',
                                           question=question,
                                           test_submit=test_submit)
            return redirect('/language/{}'.format(language_name))
        return render_template('language_challenges.html',
                               title=language_name,
                               questions=questions)
    return redirect('/dashboard')


@app.route('/dashboard')
@login_required
def dashboard():
    user = User(current_user.id, current_user.email, current_user.username, current_user.password, current_user.score)
    languages_data = db.get_languages()  # list of languages data
    languages = []  # save instances of Language
    for language_data in languages_data:
        language = Language(*language_data)
        languages.append(language)
    return render_template('dashboard.html', languages=languages, user=user)


# Homepage
@app.route('/')
def home_page():
    if current_user.is_authenticated:
        return redirect('/dashboard')
    return 'This is homepage!'


@app.route('/profile', strict_slashes=False)
@login_required
def profile():
    return render_template('profile.html')


# Login page
@app.route('/login', methods=["GET", "POST"], strict_slashes=False)
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data = db.get_user(email)
        if user_data:  # check if user is in database
            user = User(*user_data)  # create new user object
            if password == user.password:  # check password
                login_user(user)  # check password
                return redirect('/dashboard')  # redirect to dashboard if login success
    if current_user.is_authenticated:  # check if user is logged in
        return redirect('/dashboard')
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
        return redirect('/dashboard')
    return render_template('sign-up.html')


# API to run code
@app.route('/api/execute', methods=["POST"])
@login_required
def execute():
    data = request.get_json()
    script = data['script']
    question_id = data['question_id']
    question = Question(*db.get_question_by_id(question_id))  # get question's info
    question.question_score = db.get_score_by_id(question.level_id)
    question_result = question.question_result.split("|")
    question_language = str()
    result = dict()
    if question.language_id == 1:  # to send to jdoodle API
        question_language = 'python3'
        version_index = 2  # newest version of Python IDE
    elif question.language_id == 2:  # to send to jdoodle API
        question_language = 'java'
        version_index = 2  # newest version of Java IDE
    if question.question_input:  # if question has input
        for _input in question.question_input.split('|'):
            stdin = _input.replace(',', '''
''')
            result = services.api_execute.compile_code(
                script=script,
                language=question_language,
                stdin=stdin,
                version=version_index
            )
            if result['output']:
                output = deepcopy(result)['output'].replace('\n', '')
                if output in question_result:
                    result['message'] = 'Success!'
                else:
                    result['message'] = 'Error!'
                    break
            else:
                result['message'] = 'Error!'
    else:
        result = services.api_execute.compile_code(
            script=script,
            language=question_language,
            stdin=None,
            version=2
        )
        if result['output']:  # check if output is null or not
            output = deepcopy(result)['output'].replace('\n', '')
            if output == question.question_result:  # check if output equals result in DB
                result['message'] = 'Success!'
            else:
                result['message'] = 'Error!'
        else:
            result['message'] = 'Error!'
    test_status = 0
    if result['message'] == 'Success!':
        test_status = 1
    current_user_id = int(current_user.get_id())  # get id of logged-in user
    get_user_question = db.get_userquestion(current_user_id, question_id)
    if get_user_question:  # if user solved this question before
        userquestion = UserQuestion(*get_user_question)
        if userquestion.test_status == 1:  # in case test_submit = 1 but user runs code again and it is wrong
            test_status = 1
        else:
            if test_status == 1:
                db.add_score(current_user_id, question.question_score)  # add score to user
        db.update_userquestion(current_user_id, question_id, test_status, script)  # update test_status
    else:
        db.add_to_userquestion(current_user_id, question_id, test_status, script)  # add to table userquestion
        if test_status == 1:
            db.add_score(current_user_id, question.question_score)  # add score to user
    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True)
