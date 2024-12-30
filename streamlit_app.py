import streamlit as st
import random
from quiz_data import get_questions
from question_model import Question
from quiz_brain import QuizBrain

def main():
    st.set_page_config(page_title="Neuroscience Quiz", page_icon="🧠")
    st.title("Brain Buzz")

    # Initialize the quiz only after the user selects the number of questions
    if 'quiz' not in st.session_state:
        select_num_questions()

    # Display the current question or show the results if the quiz is over
    if st.session_state.quiz.has_questions():
        display_question()
    else:
        display_results()

def select_num_questions():
    # Add a selector for the number of questions
    num_questions = st.selectbox(
        "Select number of questions:",
        [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        index=0  # Default to 10 questions
    )
    
    # Fetch questions based on the user's selection
    question_data = get_questions()  # Assume this returns all questions
    # Randomly shuffle and select a subset of questions based on the user's choice
    random.shuffle(question_data)
    selected_questions = question_data[:num_questions]

    # Initialize quiz with selected questions
    question_bank = [Question(q['question'], q['incorrect_answers'] + [q['correct_answer']], q['correct_answer']) for q in selected_questions]
    st.session_state.quiz = QuizBrain(question_bank)
    st.session_state.quiz.set_question_number(num_questions)  # Set the number of questions
    st.session_state.current_question = st.session_state.quiz.next_question()
    st.session_state.time_left = 30
    st.session_state.answered = False
    st.session_state.background_color = get_random_light_color()
    st.session_state.questions_completed = 0  # Initialize the number of completed questions

def display_question():
    set_background_color(st.session_state.background_color)

    # Display the progress (questions completed / total questions)
    st.write(f"Question {st.session_state.questions_completed + 1}/{st.session_state.quiz.total_questions}")
    
    if st.session_state.time_left > 0 and not st.session_state.answered:
        st.write(st.session_state.current_question.text)

        # Display choices as buttons
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
        st.session_state.questions_completed += 1  # Increment the number of questions completed
    else:
        st.session_state.quiz_completed = True

def display_results():
    set_background_color("#FFFFFF")  # Reset to white background for results page
    st.write("You've completed the quiz!")
    st.write(f"Your final score is: {st.session_state.quiz.score}/{st.session_state.quiz.total_questions}")
    if st.button("Restart Quiz"):
        st.session_state.clear()
        st.experimental_rerun()

def get_random_light_color():
    # Generate a random light color
    r = random.randint(200, 255)
    g = random.randint(200, 255)
    b = random.randint(200, 255)
    return f"rgb({r},{g},{b})"

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
