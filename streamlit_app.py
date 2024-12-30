import streamlit as st
import random
from quiz_data import get_questions
from question_model import Question
from quiz_brain import QuizBrain

def main():
    st.set_page_config(page_title="Brain Buzz Neuroscience Quiz", page_icon="🧠")
    st.title("Brain Buzz")
    st.markdown(
        """
        <style>
        body {
            background-color: #ffcccc;  /*  red background */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if 'quiz' not in st.session_state:
        initialize_quiz()

    if st.session_state.quiz.has_questions():
        display_question()
    else:
        display_results()

def initialize_quiz():
    question_data = get_questions()
    question_bank = [Question(q['question'], q['incorrect_answers'] + [q['correct_answer']], q['correct_answer']) for q in question_data]
    st.session_state.quiz = QuizBrain(question_bank)
    st.session_state.quiz.set_question_number(10)  # Default to 10 questions, you can make this configurable
    st.session_state.current_question = st.session_state.quiz.next_question()
    st.session_state.time_left = 30
    st.session_state.answered = False

def display_question():
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
    else:
        st.session_state.quiz_completed = True

def display_results():
    st.write("You've completed the quiz!")
    st.write(f"Your final score is: {st.session_state.quiz.score}/{st.session_state.quiz.question_number}")
    if st.button("Restart Quiz"):
        st.session_state.clear()
        st.experimental_rerun()

if __name__ == "__main__":
    main()
