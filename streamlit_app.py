import streamlit as st
import random
from quiz_data import get_questions
from question_model import Question
from quiz_brain import QuizBrain

def get_random_light_color():
  """Generates a random light color in RGB format"""
  r = random.randint(200, 255)
  g = random.randint(200, 255)
  b = random.randint(200, 255)
  return f"rgb({r},{g},{b})"

def initialize_quiz():
  """Initializes the quiz with questions and sets state variables"""
  question_data = get_questions()
  question_bank = [Question(q['question'], q['incorrect_answers'] + [q['correct_answer']], q['correct_answer']) for q in question_data]
  st.session_state.quiz = QuizBrain(question_bank)
  st.session_state.quiz.set_question_number(st.session_state.question_count)
  st.session_state.current_question = st.session_state.quiz.next_question()
  st.session_state.time_left = 30
  st.session_state.answered = False
  st.session_state.background_color = get_random_light_color()

def main():
    st.set_page_config(page_title="Neuroscience Quiz", page_icon="🧠")
    st.title("Brain Buzz")

    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'quiz' not in st.session_state:
        st.session_state.quiz = None
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'time_left' not in st.session_state:
        st.session_state.time_left = 30
    if 'answered' not in st.session_state:
        st.session_state.answered = False
    if 'background_color' not in st.session_state:
        st.session_state.background_color = get_random_light_color()

    if not st.session_state.quiz_started:
        choose_question_count()
    elif st.session_state.quiz is None:
        initialize_quiz()
    elif st.session_state.quiz.has_questions():
        display_question()
    else:
        display_results()

def choose_question_count():
    # ... (choose_question_count function remains the same)

# ... (rest of your code remains the same) 

if __name__ == "__main__":
    main()
