from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import sqlite3
import os
from groq import Groq
import re
import httpx

client = Groq(
    api_key="your_key",
    http_client=httpx.Client(verify=False)
)

def get_groq_response(question, prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ]
    )
    raw = response.choices[0].message.content.strip()

    match = re.search(r"```(?:sql)?\s*(.*?)```", raw, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    for line in raw.splitlines():
        line = line.strip()
        if line.upper().startswith(("SELECT", "INSERT", "UPDATE", "DELETE", "CREATE")):
            return line

    return raw

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows

prompt = """
You are an expert in converting English questions to SQL queries.
The SQL database is named STUDENT and has columns: NAME, CLASS, SECTION.

Rules:
- Return ONLY the raw SQL query, nothing else.
- No explanations, no markdown, no code blocks, no extra text.
- Do not include the word 'sql' or backticks.

Examples:
Question: How many entries of records are present?
SELECT COUNT(*) FROM STUDENT;

Question: What are the names of students in datascience class?
SELECT * FROM STUDENT WHERE CLASS='datascience';
"""

st.set_page_config(page_title="SQL Query Retriever")
st.header("Groq App to Retrieve SQL Data")

question = st.text_input("Input your question:", key="question")
submit = st.button("Submit")

if submit:
    sql = get_groq_response(question, prompt)
    st.caption(f"Generated SQL: `{sql}`")
    try:
        rows = read_sql_query(sql, r'C:\Users\Admin\Desktop\End to End Gen AI Project using Google Gemini Pro\Students.db')
        st.subheader("The response is:")
        if rows:
            for row in rows:
                st.write(row)
        else:
            st.write("No results found.")
    except Exception as e:
        st.error(f"SQL Error: {e}\nGenerated SQL: {sql}")