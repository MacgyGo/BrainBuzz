import streamlit as st
import random
from quiz_data import get_questions
from question_model import Question
from quiz_brain import QuizBrain
import time

def get_random_light_color():
    """Generates a random light color in RGB format"""
    r = random.randint(200, 255)
    g = random.randint(200, 255)
    b = random.randint(200, 255)
    return f"rgb({r},{g},{b})"

def initialize_quiz():
    """Initializes the quiz with questions and sets state variables"""
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
    st.session_state.time_left = 30
    st.session_state.answered = False
    st.session_state.background_color = get_random_light_color()
    st.session_state.current_index = 0

def main():
    st.set_page_config(page_title="Neuroscience Quiz", page_icon="🧠")
    st.title("Brain Buzz")

    for key in ['quiz_started', 'question_count', 'quiz_data', 'current_index', 'quiz', 'time_left']:
        if key not in st.session_state:
            st.session_state[key] = None if key in ['quiz_data', 'quiz'] else False

    if not st.session_state.quiz_started:
        choose_question_count()
    else:
        if st.session_state.quiz is None:
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
        st.session_state.current_index = 0
        st.session_state.time_left = 30

        

def display_question():
    set_background_color(st.session_state.background_color)

    st.write(f"Question {st.session_state.current_index + 1}/{st.session_state.question_count}")
    st.progress((st.session_state.current_index + 1) / st.session_state.question_count)
    st.write(st.session_state.current_question.text)

    # Create a placeholder for the timer
    timer_placeholder = st.empty()

    # JavaScript to update the timer
    st.markdown(
        """
        <script>
            var timer = 30;
            var timerElement = document.getElementById('timer');
            var interval = setInterval(function() {
                timer--;
                if (timer >= 0) {
                    timerElement.textContent = timer;
                } else {
                    clearInterval(interval);
                    timerElement.textContent = "Time's up!";
                    // Use Streamlit's postMessage to notify Python
                    window.parent.postMessage({type: "streamlit:timeUp"}, "*");
                }
            }, 1000);
        </script>
        """,
        unsafe_allow_html=True
    )

    # Display the timer
    timer_placeholder.markdown('<p>Time left: <span id="timer">30</span> seconds</p>', unsafe_allow_html=True)

    for i, choice in enumerate(st.session_state.current_question.choices):
        if st.button(choice, key=f"choice_{i}"):
            check_answer(choice)

    # Check for time's up message
    if st.session_state.get('time_up', False):
        check_answer(None)
        st.session_state.time_up = False

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

    if st.button("Next Question"):
        next_question()

def next_question():
    if st.session_state.quiz.has_questions():
        st.session_state.current_question = st.session_state.quiz.next_question()
        st.session_state.time_left = 30
        st.session_state.answered = False
        st.session_state.background_color = get_random_light_color()
        st.session_state.current_index += 1
        st.experimental_rerun()
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

    # Handle JavaScript messages
    if st.session_state.quiz_started:
        message = st.experimental_get_query_params().get("streamlitMessage")
        if message and message[0] == "timeUp":
            st.session_state.time_up = True
            st.experimental_rerun()
