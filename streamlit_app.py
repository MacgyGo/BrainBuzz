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

    if not st.session_state.quiz_started:
        choose_question_count()
    elif 'quiz' not in st.session_state:
        initialize_quiz()
    elif st.session_state.quiz.has_questions():
        display_question()
    else:
        display_results()

def choose_question_count():
    question_data = get_questions()
    max_questions = len(question_data)
    st.write(f"Total available questions: {max_questions}")
    
    question_count = st.selectbox("Choose the number of questions:", 
                                  options=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                                  index=0)
    
    if st.button("Start Quiz"):
        st.session_state.question_count = min(question_count, max_questions)
        st.session_state.quiz_started = True
        st.rerun()

def initialize_quiz():
    question_data = get_questions()
    question_bank = [Question(q['question'], q['incorrect_answers'] + [q['correct_answer']], q['correct_answer']) for q in question_data]
    st.session_state.quiz = QuizBrain(question_bank)
    st.session_state.quiz.set_question_number(st.session_state.question_count)
    st.session_state.current_question = st.session_state.quiz.next_question()
    st.session_state.time_left = 30
    st.session_state.answered = False
    st.session_state.background_color = get_random_light_color()

# ... (rest of the functions remain the same)

if __name__ == "__main__":
    main()
