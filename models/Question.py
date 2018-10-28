class Question:
    def __init__(self, question_id, question_name, question_content, level_id,
                 language_id, question_input, question_result):
        self.question_id = question_id
        self.question_name = question_name
        self.question_content = question_content
        self.level_id = level_id
        self.language_id = language_id
        self.question_input = question_input
        self.question_result = question_result
        self.question_score = None
        self.question_level = None
        self.question_language = None
