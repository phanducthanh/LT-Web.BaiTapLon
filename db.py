import sqlite3


def connect():
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.close()


def add_user(username, email, password):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.execute(
        'INSERT INTO User (email, username, password, score) VALUES (?, ?, ?, ?)',
        (username, email, password, 0)
    )
    conn.commit()
    conn.close()


def get_user(email):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.execute(
        'SELECT * FROM User WHERE email = ?', (email, )
    )
    fetched = c.fetchone()
    conn.close()
    if fetched:
        return fetched
    return


get_user("trandatdt")


# Get user by id for LoginManager
def get_user_by_id(user_id):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.execute(
        'SELECT * FROM User WHERE id = ?', (user_id,)
    )
    fetched = c.fetchone()
    conn.close()
    if fetched:
        return fetched
    return
