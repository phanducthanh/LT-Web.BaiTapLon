from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id, username, email, password, score):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.score = score

    def get_password(self):
        return self.password

    def check_password(self, password):
        if password == self.password:
            return True
        return False
