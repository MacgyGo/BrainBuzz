import streamlit as st
import random
from quiz_data import get_questions
from question_model import Question
from quiz_brain import QuizBrain

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
    question_data = get_questions()
    max_questions = len(question_data)
    st.write(f"Total available questions: {max_questions}")

    # Allow users to choose any number between 1 and max_questions
    question_count = st.slider(
        "Choose the number of questions:", 
        min_value=1, 
        max_value=max_questions, 
        step=1, 
        value=10
    )

    if st.button("Start Quiz"):
        st.session_state.question_count = question_count
        st.session_state.quiz_started = True
        st.rerun()

# ... (rest of your code remains the same) 

if __name__ == "__main__":
    main()
