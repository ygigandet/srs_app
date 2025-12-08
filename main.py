# pylint: disable=missing-module-docstring

import logging
import os
from datetime import date, timedelta
import json
import subprocess

import duckdb
import pandas as pd
import streamlit as st
from streamlit_ace import st_ace

from init_json import memory_state_python_df

if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("Creating data folder")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    with open("init_db.py", "r", encoding="utf-8") as f:
        exec(f.read())  # pylint: disable=exec-used

if "drilling_machine1.json" not in os.listdir("data"):
    with open("init_json.py", "r", encoding="utf-8") as f:
        exec(f.read())

st.write(
    """
# SRS - Space repetition system 

Application for reviewing programming languages
"""
)

with st.sidebar:
    selected_language = st.selectbox(
        "Select programming language:",
        ["SQL", "Python"],
        index=None,
        placeholder="Select programming language"
    )
    if selected_language == "SQL":
        con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)
        available_theme_df = con.execute("SELECT * FROM memory_state").df()
        available_theme = available_theme_df[
            pd.to_datetime(available_theme_df["last_reviewed"]).dt.date <= date.today()
        ]["theme"].unique()
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
        exercise_name_selected = exercise_selected.loc[0, "exercise_name"]
    if selected_language == "Python":
        memory_state_python = memory_state_python_df
        available_theme = memory_state_python[
            pd.to_datetime(memory_state_python["last_reviewed"]).dt.date <= date.today()
            ]["theme"].unique()
        selected_theme = st.selectbox(
            "Select theme:",
            available_theme,
            index=None,
            placeholder="Select theme",
        )

if selected_language == "SQL":
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

    with tab2:
        exercise_instructions = exercise_selected.loc[0, "instructions"]
        with open(f"instructions/{exercise_instructions}", "r", encoding="utf-8") as f:
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
elif selected_language == "Python":
    with open("data/drilling_machine1.json") as f:
        data = json.load(f)
    tab1, tab2, tab3, tab4 = st.tabs(["Exercise", "JSON file", "Expected result", "Solution"])

    with tab1:
        code = st_ace(
            language = selected_language,
            show_gutter = True,
            key = "editor"
        )
        drilling_machine = memory_state_python_df
        if st.button("Run code"):
            try:
                with open("tempo_code.py", "w") as f:
                    f.write(code)

                result = subprocess.run(["python", "tempo_code.py"], capture_output=True, text=True)

                st.subheader("Output:")
                st.text(result.stdout)
                if result.stderr:
                    st.error(result.stderr)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Currently, only Python code execution is supported.")

    with tab2:
        st.json(data)

    with tab3:
        st.write("Tab3")

    with tab4:
        st.write("Tab4")
else:
    st.write("Choose a language!")
