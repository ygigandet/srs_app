# pylint: disable=missing-module-docstring

import os
import logging
import duckdb
import streamlit as st

if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("Creating data folder")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

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

query = st.text_area("Write your query here")

tab1, tab2, tab3, tab4 = st.tabs(["Exercise", "Tables", "Expected result", "Solution"])

with tab1:
    exercise_title = exercise.loc[0, "title"]
    st.write(exercise_title)
    if query:
        result_user = con.execute(query).df()
        st.dataframe(result_user)

with tab2:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"Table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    exercise_answer = exercise.loc[0, "answer"]
    with open(f"answers/{exercise_answer}", "r", encoding="utf-8") as f:
        answer = f.read()
    exercise_answer_query = con.execute(answer)
    st.dataframe(exercise_answer_query)

with tab4:
    st.text(answer)
