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
        st.session_state.background_color = "white" 

    if not st.session_state.quiz_started:
        choose_question_count()
    elif st.session_state.quiz is None:
        initialize_quiz()
    elif st.session_state.quiz.has_questions():
        display_question()
    else:
        display_results()

def choose_question_count():
    question_data = get_questions()
    max_questions = len(question_data)
    st.write(f"Total available questions: {max_questions}")

    question_count = st.slider(
        "Choose the number of questions:", 
        min_value=1, 
        max_value=min(max_questions, 100), 
        step=1, 
        value=10
    )

    if st.button("Start Quiz"):
        st.session_state.question_count = question_count
        st.session_state.quiz_started = True
        st.experimental_rerun()  # Use experimental_rerun() for proper reruns

def display_question():
    set_background_color(st.session_state.background_color)

    if st.session_state.time_left > 0 and not st.session_state.answered:
        st.write(f"Question {st.session_state.quiz.question_number}/{st.session_state.quiz.total_questions}")
        st.write(st.session_state.current_question.text)

        for i, choice in enumerate(st.session_state.current_question.choices):
            if st.button(choice, key=f"choice_{i}"):
                check_answer(choice)

        st.write(f"Time left: {st.session_state.time_left} seconds")
        st.session_state.time_left -= 1
    elif not st.session_state.answered:
        st.write("Time's up!")
        check_answer(None)

    if st.session_state.answered:
        if st.button("Next Question"):
            next_question()

def check_answer(user_answer):
    st.session_state.answered = True
    if user_answer:
        is_correct = st.session_state.quiz.check_answer(user_answer)
        if is_correct:
            st.success("Correct!")
        else:
            st.error("Wrong!")
            st.write(f"The correct answer was: {st.session_state.quiz.get_correct_answer()}")
    else:
        st.error("Time's up!")
        st.write(f"The correct answer was: {st.session_state.quiz.get_correct_answer()}")

def next_question():
    if st.session_state.quiz.has_questions():
        st.session_state.current_question = st.session_state.quiz.next_question()
        st.session_state.time_left = 30
        st.session_state.answered = False
        st.session_state.background_color = get_random_light_color()
    else:
        st.session_state.quiz_completed = True

def display_results():
    set_background_color("#FFFFFF")  # Reset to white background for results page
    st.write("You've completed the quiz!")
    st.write(f"Your final score is: {st.session_state.quiz.score}/{st.session_state.quiz.question_number}") 
    if st.button("Restart Quiz"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

def set_background_color(color):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
