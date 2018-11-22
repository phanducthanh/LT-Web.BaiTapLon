class Result:
    def __init__(self, user_id, question_id, test_status, test_submit, memory, cpu_time, result_price):
        self.user_id = user_id
        self.question_id = question_id
        self.memory = memory
        self.cpu_time = cpu_time
        self.result_price = result_price
        self.test_status = test_status
        self.test_submit = test_submit
