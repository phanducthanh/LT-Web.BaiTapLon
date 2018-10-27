class Question:
    def __init__(self, question_id, question_name, question_content, level,
                 language, question_input, question_result):
        self.question_id = question_id
        self.question_name = question_name
        self.question_content = question_content
        self.level = level
        self.language = language
        self.question_input = question_input
        self.question_result = question_result
        self.score = 0
