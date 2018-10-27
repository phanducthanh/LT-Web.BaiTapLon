import mysql.connector


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
        'SELECT question_id, question_name, question_content, level_name, language_name, question_input, question_result FROM question, questionlevel, language WHERE question.language_id = %s AND question.level_id = question.level_id GROUP BY question_id',
        (language_id,)
    )
    questions = cursor.fetchall()
    cursor.close()
    cnx.close()
    return questions


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
