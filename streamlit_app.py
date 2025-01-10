import time

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

        st.write(f"Time left: {st.session_state.time_left} seconds")
        st.session_state.time_left -= 1  # Decrement time

        # Rerun to update the timer every second
        time.sleep(1)  # Pause for 1 second
        st.experimental_rerun()  # Trigger rerun to update the timer

    elif not st.session_state.answered:
        st.write("Time's up!")
        check_answer(None)  # Handle unanswered case

    # Provide option to proceed to the next question
    if st.session_state.answered:
        if st.button("Next Question"):
            next_question()
