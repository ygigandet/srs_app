# pylint: disable=missing-module-docstring

import duckdb
import streamlit as st

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
        select_exercise_query = f"SELECT * FROM memory_state"
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
    with open(f"answers/{exercise_answer}", "r") as f:
        answer = f.read()
    exercise_answer_query = con.execute(answer)
    st.dataframe(exercise_answer_query)

with tab4:
    st.text(answer)

# This will be done when we have multiple languages for the application

# with st.sidebar:
#     option_languages = st.selectbox(
#         "What would you like to review?",
#         ["SQL"],
#         index=None,
#         placeholder="Select programming language",
#     )
#
#     if option_languages == "SQL":
#         st.selectbox(
#             "Select themes",
#             ("cross_joins", "inner_joins"),
#             index=None,
#             placeholder="Select the theme you want to review",
#         )
#     else:
#         st.selectbox(
#             "Select themes", (), index=None, placeholder="This is not done yet"
#         )
#
# if option_languages == "SQL":
#     query = st.text_area("Enter your query")
