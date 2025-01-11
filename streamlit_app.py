import streamlit as st
import random
from quiz_data import get_questions
from question_model import Question
from quiz_brain import QuizBrain
import asyncio
import time


def get_random_light_color():
    """Generates a random light color in RGB format"""
    r = random.randint(200, 255)
    g = random.randint(200, 255)
    b = random.randint(200, 255)
    return f"rgb({r},{g},{b})"

def initialize_quiz():
    """Initializes the quiz with questions and sets state variables"""
    # Load questions into session state if not already loaded
    #if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = get_questions()

    # Validate that quiz_data is not empty or None
    if not st.session_state.quiz_data:
        st.error("No questions available. Please check the data source.")
        return  # Exit function if no quiz data is available

    # Create a question bank from the quiz data
    question_bank = [
        Question(q['question'], q['incorrect_answers'] + [q['correct_answer']], q['correct_answer'])
        for q in st.session_state.quiz_data
    ]

    # Initialize the QuizBrain object and other session state variables
    st.session_state.quiz = QuizBrain(question_bank)
    st.session_state.quiz.set_question_number(st.session_state.question_count)
    st.session_state.current_question = st.session_state.quiz.next_question()
    st.session_state.time_left = 30  # Set timer for each question
    st.session_state.answered = False  # Indicates whether the current question is answered
    st.session_state.background_color = get_random_light_color()  # Randomize background color
    st.session_state.current_index = 0  # Track the index of the current question

def main():
    # Configure the Streamlit app
    st.set_page_config(page_title="Neuroscience Quiz", page_icon="🧠")
    st.title("Brain Buzz")

    # Initialize session state variables if they are not already set
    for key in ['quiz_started', 'question_count', 'quiz_data', 'current_index', 'quiz']:
        if key not in st.session_state:
            st.session_state[key] = None if key in ['quiz_data', 'quiz'] else False

    # Handle the state of the quiz (start, progress, results)
    if not st.session_state.quiz_started:
        choose_question_count()  # Allow user to choose the number of questions
    else:
        # Ensure the quiz is initialized before proceeding
        if st.session_state.quiz is None:
            initialize_quiz()

        # Display questions or results based on quiz state
        if st.session_state.quiz and st.session_state.quiz.has_questions():
            display_question()
        
  
 

        else:
            display_results()


def choose_question_count():
    """Displays a slider for the user to choose the number of quiz questions"""
    question_data = get_questions()
    max_questions = len(question_data)
    st.write(f"Total available questions: {max_questions}")

    # Slider for selecting the number of questions
    question_count = st.slider(
        "Choose the number of questions:",
        min_value=1,
        max_value=min(max_questions, 100),
        step=1,
        value=10
    )

    # Start the quiz when the button is clicked
    if st.button("Start Quiz"):
        st.session_state.question_count = question_count
        st.session_state.quiz_started = True
        st.session_state.current_index = 0  # Reset the current index

        # Handle reruns for both newer and older Streamlit versions
        if hasattr(st, 'experimental_rerun'):
            st.experimental_rerun()
        else:
            st.empty()  # Trigger a re-render for older versions

def display_question():
    """Displays the current question and its answer choices"""
    set_background_color(st.session_state.background_color)  # Set dynamic background color

    # Show question and track time if unanswered
    if st.session_state.time_left > 0 and not st.session_state.answered:
        st.write(f"Question {st.session_state.current_index + 1}/{st.session_state.question_count}")
        st.progress((st.session_state.current_index + 1) / st.session_state.question_count)
        st.write(st.session_state.current_question.text)  # Display question text

        # Display answer choices as buttons
        for i, choice in enumerate(st.session_state.current_question.choices):
            if st.button(choice, key=f"choice_{i}"):
                check_answer(choice)  # Handle answer selection

        # st.write(f"Time left: {st.session_state.time_left} seconds")
        # st.session_state.time_left -= 1  # Decrement time
        
        with st.empty():
            for seconds in range(10):
                st.write(f"⏳ {seconds} seconds have passed")
                time.sleep(1)
            st.write("✔️ time up!")

    elif not st.session_state.answered:
        st.write("Time's up!")
        check_answer(None)  # Handle unanswered case

    # Provide option to proceed to the next question
    if st.session_state.answered:

        if st.button("Next Question"):
            next_question()

def check_answer(user_answer):
    """Checks the user's answer and displays feedback"""
    st.session_state.answered = True  # Mark the question as answered
    st.empty()  # clear the timer
    if user_answer:
        is_correct = st.session_state.quiz.check_answer(user_answer)  # Check answer correctness
        if is_correct:
            st.success("Correct!")
        else:
            st.error("Wrong!")
            st.write(f"The correct answer was: {st.session_state.quiz.get_correct_answer()}")
    else:
        st.error("Time's up!")
        st.write(f"The correct answer was: {st.session_state.quiz.get_correct_answer()}")

def next_question():
    """Loads the next question or marks the quiz as completed"""
    if st.session_state.quiz.has_questions():
        st.session_state.current_question = st.session_state.quiz.next_question()
        st.session_state.time_left = 30  # Reset timer
        st.session_state.answered = False  # Reset answered state
        st.session_state.background_color = get_random_light_color()  # Randomize background color
        st.session_state.current_index += 1  # Increment question index
    else:
        st.session_state.quiz_completed = True  # Mark quiz as completed

def display_results():
    """Displays the final results of the quiz"""
    set_background_color("#FFFFFF")  # Reset to white background for results page
    st.write("You've completed the quiz!")
    st.write(f"Your final score is: {st.session_state.quiz.score}/{st.session_state.question_count}")

    # Provide option to restart the quiz
    if st.button("Restart Quiz"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]  # Clear session state
        if hasattr(st, 'experimental_rerun'):
            st.experimental_rerun()
        else:
            st.empty()  # Trigger a re-render for older versions

def set_background_color(color):
    """Sets the background color of the app dynamically"""
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
