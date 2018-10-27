# This is test file :D

from models.Language import Language

li = [Language(1, 'Python', 'Bla bla 1'), Language(2, 'Java', 'Bla bla 2')]

for i in li:
    print(i.language_name)
