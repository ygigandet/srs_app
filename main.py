# pylint: disable=missing-module-docstring

import logging
import os

from datetime import date, timedelta
import duckdb
import streamlit as st

if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("Creating data folder")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    with open("init_db.py", "r", encoding="utf-8") as f:
        exec(f.read())  # pylint: disable=exec-used

st.write(
    """
# SRS - Space repetition system 

Application for reviewing programming languages
"""
)

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    available_theme_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    theme = st.selectbox(
        "Select theme:",
        available_theme_df["theme"].unique(),
        index=None,
        placeholder="Select theme",
    )
    if theme:
        select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        select_exercise_query = "SELECT * FROM memory_state"
    exercise = (
        con.execute(select_exercise_query)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )

tab1, tab2, tab3, tab4 = st.tabs(["Exercise", "Tables", "Expected result", "Solution"])

with tab1:
    query = st.text_area("Write your query here")
    if query:
        result_user = con.execute(query).df()
        st.dataframe(result_user)
    exercise_answer = exercise_selected.loc[0, "answer"]
    with open(f"answers/{exercise_answer}", "r", encoding="utf-8") as f:
        answer = f.read()
    if query == answer:
        st.write("Yes, that's it!")
    for n_days in [2, 7, 21]:
        if st.button(f"Review in {n_days} days"):
            next_review = date.today() + timedelta(days=n_days)
            con.execute(f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name = '{exercise_name_selected}'")
            st.rerun()

with tab2:
    exercise_instructions = exercise_selected.loc[0, "instructions"]
    with open(f"instructions/{exercise_instructions}", "r") as f:
        instructions = f.read()
    st.text(instructions)
    exercise_tables = exercise_selected.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"Table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    exercise_answer_query = con.execute(answer)
    st.dataframe(exercise_answer_query)

with tab4:
    st.text(answer)
