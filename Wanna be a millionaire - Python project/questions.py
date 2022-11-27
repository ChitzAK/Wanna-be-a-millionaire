
class Question:
    def __init__(self, question_text: str, first_answer: str,
                 second_answer: str, third_answer: str, fourth_answer: str, correct_answer: str):
        self.question_text = question_text
        self.first_answer = first_answer
        self.second_answer = second_answer
        self.third_answer = third_answer
        self.fourth_answer = fourth_answer
        self.correct_answer = correct_answer

    def is_correct(self, user_answer: str):
        """Returns a boolean"""
        return self.correct_answer.__eq__(user_answer)
