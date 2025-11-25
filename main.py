import streamlit as st
import duckdb

st.write("""
SRS - Space repetition system application for reviewing programming languages""")

# It will need to be modified !!!
con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

option_languages = st.selectbox(
    "What would you like to review?",
    ("SQL", "Python"),
    index=None,
    placeholder="Select programming language",
)

if option_languages == "SQL":
    st.selectbox(
        "Select themes",
        ("cross_joins", "inner_joins"),
        index=None,
        placeholder="Select the theme you want to review"
    )
else:
    st.selectbox(
        "Select themes",
        (),
        index=None,
        placeholder="This is not done yet"
    )

# query = st.text_area("Enter your query")
#
# if query:
#     result_user = con.execute(query).df()
#     st.dataframe(result_user)
