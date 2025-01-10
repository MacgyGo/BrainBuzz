import streamlit as st
import random
from quiz_data import get_questions
from question_model import Question
from quiz_brain import QuizBrain
import time

def get_random_light_color():
    r = random.randint(200, 255)
    g = random.randint(200, 255)
    b = random.randint(200, 255)
    return f"rgb({r},{g},{b})"

def initialize_quiz():
    st.session_state.quiz_data = get_questions()
    if not st.session_state.quiz_data:
        st.error("No questions available. Please check the data source.")
        return

    question_bank = [
        Question(q['question'], q['incorrect_answers'] + [q['correct_answer']], q['correct_answer'])
        for q in st.session_state.quiz_data
    ]

    st.session_state.quiz = QuizBrain(question_bank)
    st.session_state.quiz.set_question_number(st.session_state.question_count)
    st.session_state.current_question = st.session_state.quiz.next_question()
    st.session_state.answered = False
    st.session_state.background_color = get_random_light_color()
    st.session_state.current_index = 0
    st.session_state.start_time = time.time()

def main():
    st.set_page_config(page_title="Neuroscience Quiz", page_icon="🧠")
    st.title("Brain Buzz")

    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False

    if not st.session_state.quiz_started:
        choose_question_count()
    else:
        if 'quiz' not in st.session_state:
            initialize_quiz()

        if st.session_state.quiz and st.session_state.quiz.has_questions():
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
        st.experimental_rerun()

def display_question():
    set_background_color(st.session_state.background_color)

    st.write(f"Question {st.session_state.current_index + 1}/{st.session_state.question_count}")
    st.progress((st.session_state.current_index + 1) / st.session_state.question_count)
    st.write(st.session_state.current_question.text)

    time_left = max(0, 30 - int(time.time() - st.session_state.start_time))
    st.write(f"Time left: {time_left} seconds")

    for choice in st.session_state.current_question.choices:
        if st.button(choice, key=choice):
            check_answer(choice)

    if time_left == 0 and not st.session_state.answered:
        check_answer(None)

    if st.session_state.answered:
        if st.button("Next Question"):
            next_question()
            st.experimental_rerun()

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
        st.session_state.answered = False
        st.session_state.background_color = get_random_light_color()
        st.session_state.current_index += 1
        st.session_state.start_time = time.time()
    else:
        st.session_state.quiz_completed = True

def display_results():
    set_background_color("#FFFFFF")
    st.write("You've completed the quiz!")
    st.write(f"Your final score is: {st.session_state.quiz.score}/{st.session_state.question_count}")

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
