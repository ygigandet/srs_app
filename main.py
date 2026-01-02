# pylint: disable=missing-module-docstring

import logging
import os
from datetime import date, timedelta

import duckdb
import pandas as pd
import streamlit as st


# ------------------------------------------------------------
# USER LOGIN (works locally & free Streamlit Cloud)
# ------------------------------------------------------------
def get_user_id():
    """
    Simple login system for free Streamlit Cloud.
    """
    if "user_id" not in st.session_state:
        username = st.text_input("Enter your username", key="login_input")
        login_pressed = st.button("Login")
        if login_pressed:
            username = username.strip()
            if username != "":
                st.session_state.user_id = username
            else:
                st.warning("Please enter a valid username.")
        st.stop()  # Stop until login
    return st.session_state.user_id


USER_ID = get_user_id()
st.write(f"Logged in as: {USER_ID}")

# ------------------------------------------------------------
# INITIALIZE DATA FOLDER AND DATABASE
# ------------------------------------------------------------
if "data" not in os.listdir():
    logging.info("Creating data folder")
    os.mkdir("data")

DB_PATH = "data/exercises_sql_tables.duckdb"
if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    with open("init_db.py", "r", encoding="utf-8") as f:
        # pylint: disable=exec-used
        exec(f.read())

# Connect to DuckDB
con = duckdb.connect(database=DB_PATH, read_only=False)


# ------------------------------------------------------------
# INITIALIZE USER PROGRESS
# ------------------------------------------------------------
def init_user_progress(user_id):
    """
    Add all exercises to user's progress if missing.
    """
    con.execute(
        """
        INSERT OR IGNORE INTO user_progress (user_id, exercise_name, last_reviewed)
        SELECT ?, exercise_name, DATE '1970-01-01'
        FROM exercises
        WHERE exercise_name NOT IN (
            SELECT exercise_name FROM user_progress WHERE user_id = ?
        )
    """,
        (user_id, user_id),
    )


init_user_progress(USER_ID)


# ------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------
def reset_query():
    """
    Erase the query when user selects either new theme or new exercise.
    :return:
    """
    st.session_state.query = ""


def execute_user_query(user_query: str) -> None:
    """
    Execution of the query
    :param user_query:
    :return:
    """
    if not user_query:
        return
    try:
        result_user = con.execute(user_query).df()
        st.dataframe(result_user)
    except duckdb.Error:
        st.error("There was an error executing your SQL query. Check syntax.")


def display_available_theme(user_id):
    """
    Load available themes for the user where exercises are due today or earlier.
    """
    df = con.execute(
        """
        SELECT DISTINCT e.theme
        FROM exercises 
        
        e
        JOIN user_progress up
        ON e.exercise_name = up.exercise_name
        WHERE up.user_id = ?
        AND up.last_reviewed <= ?
    """,
        (user_id, date.today()),
    ).df()

    return df["theme"].tolist()


def display_available_exercise(user_id, selected_theme_user):
    """
    Load exercises for the user in the selected theme that are due today or earlier.
    """
    df = con.execute(
        """
        SELECT e.*, up.last_reviewed
        FROM exercises e
        JOIN user_progress up
        ON e.exercise_name = up.exercise_name
        WHERE up.user_id = ?
        AND e.theme = ?
    """,
        (user_id, selected_theme_user),
    ).df()

    # Convert last_reviewed to Python date
    df["last_reviewed"] = pd.to_datetime(df["last_reviewed"]).dt.date

    # Filter exercises due today or earlier
    exercises_filtered = df[df["last_reviewed"] <= date.today()]

    # Sort by last_reviewed ascending
    exercises_filtered = exercises_filtered.sort_values("last_reviewed").reset_index(
        drop=True
    )

    return exercises_filtered


# ------------------------------------------------------------
# STREAMLIT UI
# ------------------------------------------------------------
st.title("SRS - Space Repetition System")
st.write("Application for reviewing programming languages")

# Sidebar
with st.sidebar:
    available_theme = display_available_theme(USER_ID)
    if len(available_theme) == 0:
        st.warning("No themes are available for review today.")
        st.stop()

    selected_theme = st.selectbox(
        "Select theme:",
        available_theme,
        index=None,
        placeholder="Select theme",
        on_change=reset_query,
    )
    if selected_theme is None:
        st.info("Please select a theme to see available exercises.")
        st.stop()

    exercise_selected = display_available_exercise(USER_ID, selected_theme)
    if exercise_selected.empty:
        st.warning("No exercises are available for this theme today.")
        st.stop()

    exercise_name_selected = st.selectbox(
        "Select exercise:",
        exercise_selected["exercise_name"].tolist(),
        on_change=reset_query,
    )
    current_exercise = exercise_selected[
        exercise_selected["exercise_name"] == exercise_name_selected
    ].iloc[0]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Exercise", "Tables", "Expected result", "Solution"])

# ------------------
# TAB 1: EXERCISE
# ------------------
with tab1:
    query = st.text_area("Write your query here", key="query")
    execute_user_query(query)
    exercise_answer = current_exercise["answer"]
    with open(f"answers/{exercise_answer}", "r", encoding="utf-8") as f:
        answer = f.read()
    if query == answer:
        st.write("Yes, that's it!")
        st.balloons()

    cols = st.columns(3)
    for col, n_days in zip(cols, [2, 7, 21]):
        with col:
            if st.button(f"Review in {n_days} days"):
                next_review = date.today() + timedelta(days=n_days)
                con.execute(
                    """
                    UPDATE user_progress
                    SET last_reviewed = ?
                    WHERE user_id = ?
                    AND exercise_name = ?
                """,
                    (next_review, USER_ID, exercise_name_selected),
                )

# ------------------
# TAB 2: INSTRUCTIONS AND TABLES
# ------------------
with tab2:
    exercise_instructions = current_exercise["instructions"]
    with open(f"instructions/{exercise_instructions}", "r", encoding="utf-8") as f:
        instructions = f.read()
    st.text(instructions)
    exercise_tables = current_exercise["tables"]
    for table in exercise_tables:
        st.write(f"Table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

# ------------------
# TAB 3: EXPECTED RESULT
# ------------------
with tab3:
    exercise_answer_query = con.execute(answer).df()
    st.dataframe(exercise_answer_query)

# ------------------
# TAB 4: SOLUTION
# ------------------
with tab4:
    st.text(answer)
