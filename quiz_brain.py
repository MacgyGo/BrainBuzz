import random

class QuizBrain:
    def __init__(self, question_list):
        self.question_list = question_list
        self.question_number = 0
        self.score = 0
        self.current_question = None
        self.total_questions = len(question_list)
        self.available_questions = list(range(len(question_list)))

    def set_question_number(self, num):
        self.total_questions = min(num, len(self.question_list))

    def has_questions(self):
        return self.question_number < self.total_questions and len(self.available_questions) > 0

    def next_question(self):
        if self.available_questions:
            question_index = random.choice(self.available_questions)
            self.available_questions.remove(question_index)
            self.current_question = self.question_list[question_index]
            self.question_number += 1

            # Randomize the order of choices
            choices = self.current_question.choices.copy()
            random.shuffle(choices)
            self.current_question.choices = choices

            return self.current_question
        return None

    def check_answer(self, user_answer):
        correct_answer = self.current_question.answer
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        return False

    def get_correct_answer(self):
        return self.current_question.answer
