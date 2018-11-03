import mysql.connector


def get_score_by_id(level_id):
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="140397",
        database="ltw",
        buffered=True
    )
    cursor = cnx.cursor()
    cursor.execute(
        'SELECT level_score FROM questionlevel WHERE level_id = %s', (level_id,)
    )
    fetched = cursor.fetchone()[0]
    cursor.close()
    cnx.close()
    return fetched


def add_score(user_id, score):
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="140397",
        database="ltw",
        buffered=True
    )
    cursor = cnx.cursor()
    cursor.execute(
        'SELECT score FROM user WHERE id = %s', (user_id,)
    )
    current_score = cursor.fetchone()[0]
    new_score = current_score + score
    cursor.execute(
        'UPDATE user SET score = %s WHERE id = %s', (new_score, user_id,)
    )
    cnx.commit()
    cursor.close()
    cnx.close()


def get_question_by_id(question_id):
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="140397",
        database="ltw",
        buffered=True
    )
    cursor = cnx.cursor()
    cursor.execute(
        'SELECT * FROM question WHERE question_id = %s', (question_id,)
    )
    fetched = cursor.fetchone()
    cursor.close()
    cnx.close()
    return fetched


def get_level_by_name(level_name):
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="140397",
        database="ltw",
        buffered=True
    )
    cursor = cnx.cursor()
    cursor.execute(
        'SELECT * FROM questionlevel WHERE level_name = %s', (level_name,)
    )
    fetched = cursor.fetchone()
    cursor.close()
    cnx.close()
    return fetched


def add_to_userquestion(user_id, question_id, test_status, test_submit):
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="140397",
        database="ltw",
        buffered=True
    )
    cursor = cnx.cursor()
    cursor.execute(
        'INSERT INTO userquestion (user_id, question_id, test_status, test_submit)'
        'VALUE (%s, %s, %s, %s)',
        (user_id, question_id, test_status, test_submit,)
    )
    cnx.commit()
    cursor.close()
    cnx.close()


def update_userquestion(user_id, question_id, test_status, test_submit):
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="140397",
        database="ltw",
        buffered=True
    )
    cursor = cnx.cursor()
    cursor.execute(
        'UPDATE userquestion SET test_status = %s, test_submit = %s WHERE user_id = %s AND question_id = %s',
        (test_status, test_submit, user_id, question_id)
    )
    cnx.commit()
    cursor.close()
    cnx.close()


def get_userquestion(user_id, question_id):
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="140397",
        database="ltw",
        buffered=True
    )
    cursor = cnx.cursor()
    cursor.execute(
        'SELECT * FROM userquestion WHERE user_id = %s AND question_id = %s',
        (user_id, question_id)
    )
    fetched = cursor.fetchone()
    cursor.close()
    cnx.close()
    return fetched


def get_questions_by_language_name(language_name):
    """
    Get questions by name of language
    :param language_name: Name of language
    :return: questions data
    """
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="140397",
        database="ltw",
        buffered=True
    )
    cursor = cnx.cursor()
    cursor.execute(
        'SELECT * FROM language WHERE language_name = %s', (language_name,)
    )
    fetched = cursor.fetchone()
    language_id = fetched[0]
    cursor.execute(
        'SELECT * FROM question, questionlevel, language WHERE question.language_id = %s AND question.language_id = language.language_id',
        (language_id,)
    )
    data = cursor.fetchall()
    cursor.close()
    cnx.close()
    return data


def get_list_languages():
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="140397",
        database="ltw",
        buffered=True
    )
    cursor = cnx.cursor()
    cursor.execute(
        'SELECT language_name FROM language'
    )
    fetched = cursor.fetchall()
    cursor.close()
    cnx.close()
    language = [fetched[i][0] for i in range(len(fetched))]
    return language


def get_languages():
    """
    Get all languages from database.
    :return: list of languages data
    """
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="140397",
        database="ltw",
        buffered=True
    )
    cursor = cnx.cursor()
    cursor.execute(
        'SELECT * FROM language'
    )
    fetched = cursor.fetchall()
    cursor.close()
    cnx.close()
    return fetched


def add_user(email, username, password):
    """
    Add an user to database
    :param email: email
    :param username: username
    :param password: password
    :return: None
    """
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="140397",
        database="ltw",
        buffered=True
    )
    cursor = cnx.cursor()
    cursor.execute(
        'INSERT INTO User (email, username, password)'
        'VALUES (%s, %s, %s)',
        (email, username, password)
    )
    cnx.commit()
    cursor.close()
    cnx.close()


def get_user(email):
    """
    Get user data from table 'user' in DB
    :param email: email to get
    :return: user's data or None
    """
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="140397",
        database="ltw",
        buffered=True
    )
    cursor = cnx.cursor()
    cursor.execute(
        'SELECT * FROM user where email = %s', (email,)
    )
    fetched = cursor.fetchone()
    cursor.close()
    cnx.close()
    return fetched


# Get user by id for LoginManager
def get_user_by_id(user_id):
    """
    Get user data from table 'user' in DB. It is for Flask-Login
    :param user_id: user's id to get
    :return: user's data or None
    """
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="140397",
        database="ltw",
        buffered=True
    )
    cursor = cnx.cursor()
    cursor.execute(
        'SELECT * FROM user where id= %s', (user_id,)
    )
    fetched = cursor.fetchone()
    cursor.close()
    cnx.close()
    return fetched
