# pylint: disable=missing-module-docstring

import duckdb
import streamlit as st

st.write(
    """
# SRS - Space repetition system 

Application for reviewing programming languages
"""
)

# It will need to be modified !!!
con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    option_languages = st.selectbox(
        "What would you like to review?",
        ["SQL", "Python"],
        index=None,
        placeholder="Select programming language",
    )

    if option_languages == "SQL":
        st.selectbox(
            "Select themes",
            ("cross_joins", "inner_joins"),
            index=None,
            placeholder="Select the theme you want to review",
        )
    else:
        st.selectbox(
            "Select themes", (), index=None, placeholder="This is not done yet"
        )

if option_languages == "SQL":
    query = st.text_area("Enter your query")

tab1, tab2 = st.tabs(["Tables", "Solution"])

with tab1:
    if query:
        result_user = con.execute(query).df()
        st.dataframe(result_user)

    if option_languages == "SQL":


with tab2:
    st.write("Empty for now")
