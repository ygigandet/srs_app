# pylint: disable=missing-module-docstring

import logging
import os
from datetime import date, timedelta

import duckdb
import pandas as pd
import streamlit as st

# ------------------------------------------------------------
# INITIALIZE DATA FOLDER AND DUCKDB DATABASE
# ------------------------------------------------------------
if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("Creating data folder")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    with open("init_db.py", "r", encoding="utf-8") as f:
        exec(f.read())  # pylint: disable=exec-used


# ------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------
def execute_user_query(user_query: str) -> None:
    """
    Execute a user-provided SQL query and display the result in Streamlit.

    If the query execution fails, an error message is shown instead.
    """
    if not user_query:
        return

    try:
        result_user = con.execute(user_query).df()
        st.dataframe(result_user)
    except duckdb.Error:
        st.error(
            "There was an error executing your SQL query. "
            "Please check your syntax and try again."
        )


def display_available_theme():
    """
    Load and return available themes from the memory_state table
    """
    available_theme_df = con.execute("SELECT * FROM memory_state").df()
    return available_theme_df[
        pd.to_datetime(available_theme_df["last_reviewed"]).dt.date <= date.today()
    ]["theme"].unique()


# ------------------------------------------------------------
# STREAMLIT
# ------------------------------------------------------------
st.write(
    """
# SRS - Space repetition system 

Application for reviewing programming languages
"""
)

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# Sidebar
with st.sidebar:
    available_theme = display_available_theme()
    selected_theme = st.selectbox(
        "Select theme:",
        available_theme,
        index=None,
        placeholder="Select theme",
    )
    if selected_theme:
        select_exercise_query = (
            f"SELECT * FROM memory_state WHERE theme = '{selected_theme}'"
        )
    else:
        select_exercise_query = "SELECT * FROM memory_state"

    exercise_selected = (
        con.execute(select_exercise_query)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )

    if exercise_selected.empty:
        st.warning("No exercise available for this theme.")
        st.stop()

    exercise_name_selected = st.selectbox(
        "Select exercise:",
        exercise_selected["exercise_name"].tolist()
    )

    current_exercise = exercise_selected[
        exercise_selected["exercise_name"] == exercise_name_selected
        ].iloc[0]

# tabs
tab1, tab2, tab3, tab4 = st.tabs(["Exercise", "Tables", "Expected result", "Solution"])

# ------------------
# TAB 1: EXERCISE
# ------------------
with tab1:
    query = st.text_area("Write your query here")
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
                    f"UPDATE memory_state SET last_reviewed = '{next_review}' \
                    WHERE exercise_name = '{exercise_name_selected}'",
                )
                st.rerun()

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
    exercise_answer_query = con.execute(answer)
    st.dataframe(exercise_answer_query)

# ------------------
# TAB 3: SOLUTION
# ------------------
with tab4:
    st.text(answer)
