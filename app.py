import os
import json
from copy import deepcopy
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
import services.api_execute
from models.User import User
from models.Language import Language
from models.Question import Question
from models.Result import Result
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


@app.route('/leaderboard', strict_slashes=False)
@login_required
def leader_board():
    users_from_db = db.leader_board()
    users = []
    for user_data in users_from_db:
        users.append(User(*user_data))
    return render_template('leaderboard.html', users=enumerate(users))


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
    return  render_template('home_page.html')


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
    return  render_template('home_page.html')


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


@app.route('/list-answer', strict_slashes=False)
@app.route('/list-answer/<int:question_id>', strict_slashes=False)
@login_required
def list_answer(question_id=None):
    if question_id:
        results = list()
        user_question = db.get_userquestion_by_question_id(question_id=question_id,
                                                           current_id=current_user.id)
        if user_question:
            i = 0
            for result in user_question:
                result_user_id = result[0]
                result_question_id = result[1]
                result_test_status = result[2]
                result_test_submit = result[3]
                result_memory = result[4]
                result_cpu_time = result[5]
                result_price = db.get_score_by_question_id(question_id)
                if i == 0:
                    result_price *= 2.5
                elif i == 1:
                    result_price *= 2.0
                elif i == 2:
                    result_price *= 1.5
                else:
                    result_price *= 1.4
                result = Result(result_user_id,
                                result_question_id,
                                result_test_status,
                                result_test_submit,
                                result_memory,
                                result_cpu_time,
                                int(result_price))
                results.append(result)
                i += 1
        return render_template("list-answer.html", results=results)
    return "No question_id found"


@app.route('/purchased-items', strict_slashes=False)
@login_required
def purchased_items():
    return "Hihi"


@app.route('/buy-answer/<string:question_and_owner>', methods=["GET", "POST"], strict_slashes=False)
@login_required
def buy_answer(question_and_owner):
    if request.method == "GET":
        if question_and_owner:
            data = question_and_owner.split("-")
            question_id = int(data[0])
            owner_id = int(data[1])

            user_question = db.get_userquestion_by_question_id(question_id=question_id,
                                                               current_id=current_user.id)
            if user_question:
                buy_price = db.get_score_by_question_id(question_id)
                i = 0
                for data in user_question:
                    if owner_id == data[0] and question_id == data[1]:
                        if i == 0:
                            buy_price *= 2.5
                        elif i == 1:
                            buy_price *= 2.0
                        elif i == 2:
                            buy_price *= 1.5
                        else:
                            buy_price *= 1.4
                        break
                    i += 1
                result = Result(data[0],
                                data[1],
                                data[2],
                                data[3],
                                data[4],
                                data[5],
                                int(buy_price))
                return render_template('buy-answer.html', result=result)
            else:
                return "No result found!"
    if request.method == "POST":
        if question_and_owner:
            data = question_and_owner.split("-")
            question_id = int(data[0])
            owner_id = int(data[1])

            user_question = db.get_userquestion_by_question_id(question_id=question_id,
                                                               current_id=current_user.id)
            if user_question:
                buy_price = db.get_score_by_question_id(question_id)
                i = 0
                for data in user_question:
                    if owner_id == data[0] and question_id == data[1]:
                        if i == 0:
                            buy_price *= 2.5
                        elif i == 1:
                            buy_price *= 2.0
                        elif i == 2:
                            buy_price *= 1.5
                        else:
                            buy_price *= 1.4
                        break
                    i += 1
                current_point = db.get_user_point(current_user.id)
                if current_point - buy_price >= 0:
                    db.minus_point_of_user(current_user.id, current_point - buy_price)
                    return "Answer: "+data[3].replace("\n", "<br>")
                else:
                    return "You don't have enough points!"


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
    version_index = 0
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
            version=version_index
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
    memory = result['memory']  # memory that code uses
    cpu_time = result['cpuTime']  # cpu time of code
    if get_user_question:  # if user solved this question before
        userquestion = UserQuestion(*get_user_question)
        if userquestion.test_status == 1:  # in case test_submit = 1 but user runs code again and it is wrong
            test_status = 1
        else:
            if test_status == 1:
                db.add_score(current_user_id, question.question_score)  # add score to user
        db.update_userquestion(current_user_id, question_id, test_status,
                               script, memory, cpu_time)  # update test_status
    else:
        db.add_to_userquestion(current_user_id, question_id, test_status,
                               script, memory, cpu_time)  # add to table userquestion
        if test_status == 1:
            db.add_score(current_user_id, question.question_score)  # add score to user
    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True)
