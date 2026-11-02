import os
import re
import sqlite3
from datetime import datetime

import pandas as pd
import streamlit as st
from google import genai


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="StudentSQL AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CONFIGURATION
# =========================================================

DB_PATH = "College_Student.db"
TABLE_NAME = "College_Student"


# =========================================================
# DARK THEME
# =========================================================

st.markdown(
    """
    <style>

    /* Main application */
    .stApp {
        background-color: #07111f;
        color: #e8eef7;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #07111f;
    }

    [data-testid="stHeader"] {
        background-color: #07111f;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #06101d !important;
    }

    [data-testid="stSidebar"] > div {
        background-color: #06101d !important;
    }

    /* Text */
    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
    }

    p, label {
        color: #c0cedd !important;
    }

    /* Text area */
    textarea {
        background-color: #081725 !important;
        color: #ffffff !important;
        border: 1px solid #29445e !important;
    }

    textarea::placeholder {
        color: #71869c !important;
    }

    /* Text input */
    input {
        background-color: #081725 !important;
        color: #ffffff !important;
    }

    input::placeholder {
        color: #71869c !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #102940 !important;
        color: #f1f5f9 !important;
        border: 1px solid #29445e !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    .stButton > button:hover {
        background-color: #173d60 !important;
        border-color: #3b82f6 !important;
        color: white !important;
    }

    /* Primary button */
    .stButton > button[kind="primary"] {
        background-color: #2563eb !important;
        color: white !important;
        border: none !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #3b82f6 !important;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background-color: #0c1e32;
        border: 1px solid #1d3853;
        padding: 18px;
        border-radius: 14px;
    }

    [data-testid="stMetricLabel"] {
        color: #91a8bf !important;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid #1d3853;
        border-radius: 10px;
    }

    /* Code */
    [data-testid="stCodeBlock"] {
        border-radius: 10px;
    }

    /* Divider */
    hr {
        border-color: #1d334b !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "question" not in st.session_state:
    st.session_state.question = ""

if "sql" not in st.session_state:
    st.session_state.sql = ""

if "result" not in st.session_state:
    st.session_state.result = None

if "history" not in st.session_state:
    st.session_state.history = []


# =========================================================
# GEMINI API
# =========================================================

import os
import streamlit as st
from google import genai


def get_api_key():

    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    return os.getenv("GEMINI_API_KEY")


API_KEY = get_api_key()

GEMINI_READY = False
client = None

if API_KEY:

    try:
        client = genai.Client(api_key=API_KEY)
        GEMINI_READY = True

    except Exception as e:
        GEMINI_READY = False
        st.error(f"Gemini configuration failed: {e}")


# =========================================================
# DATABASE FUNCTIONS
# =========================================================

def database_exists():

    return os.path.exists(DB_PATH)


def get_connection():

    return sqlite3.connect(DB_PATH)


def get_student_data():

    conn = get_connection()

    try:

        df = pd.read_sql_query(
            f"SELECT * FROM {TABLE_NAME}",
            conn
        )

        return df

    finally:

        conn.close()


def get_table_info():

    conn = get_connection()

    try:

        df = pd.read_sql_query(
            f"PRAGMA table_info({TABLE_NAME})",
            conn
        )

        return df

    finally:

        conn.close()


def execute_sql(sql):

    conn = get_connection()

    try:

        df = pd.read_sql_query(
            sql,
            conn
        )

        return df

    finally:

        conn.close()


# =========================================================
# GEMINI SQL PROMPT
# =========================================================

SQL_PROMPT = """

You are an expert Text-to-SQL assistant.

Convert the user's natural language question into ONE
valid SQLite SELECT query.

DATABASE:

Database:
College_Student.db

Table:
College_Student

Columns:

ID
Name
Age
Gender
Department
CGPA

Department values may include:

CSE
IT
ECE
ME
CIVIL

Gender values:

M
F

IMPORTANT RULES:

1. Return ONLY the SQL query.
2. Do not explain anything.
3. Do not use markdown.
4. Do not use ```sql.
5. Do not use ``` anywhere.
6. Always use the exact table name College_Student.
7. Always use the exact column names.
8. Only SELECT queries are allowed.
9. WITH queries are allowed.
10. Never use INSERT.
11. Never use UPDATE.
12. Never use DELETE.
13. Never use DROP.
14. Never use ALTER.
15. Never use CREATE.
16. Never use PRAGMA.
17. Never use ATTACH.
18. Never use DETACH.
19. Never generate multiple queries.
20. Use SQLite syntax.

Examples:

Question:
How many students are there?

Answer:
SELECT COUNT(*) AS Total_Students
FROM College_Student;

Question:
Show all CSE students

Answer:
SELECT *
FROM College_Student
WHERE Department = 'CSE';

Question:
Show students with CGPA above 8

Answer:
SELECT *
FROM College_Student
WHERE CGPA > 8;

Question:
Show top 10 students

Answer:
SELECT *
FROM College_Student
ORDER BY CGPA DESC
LIMIT 10;

Question:
Average CGPA of each department

Answer:
SELECT Department,
       AVG(CGPA) AS Average_CGPA
FROM College_Student
GROUP BY Department;

Question:
How many male and female students?

Answer:
SELECT Gender,
       COUNT(*) AS Total_Students
FROM College_Student
GROUP BY Gender;

Question:
Who is the topper?

Answer:
SELECT *
FROM College_Student
ORDER BY CGPA DESC
LIMIT 1;

Now convert the user's question.

"""


# =========================================================
# GENERATE SQL
# =========================================================

def generate_sql(question):

    if not GEMINI_READY:
        raise Exception(
            "Gemini API key is not configured."
        )

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=SQL_PROMPT + "\n\nUser Question:\n" + question
    )

    if not response or not response.text:
        raise Exception(
            "Gemini returned an empty response."
        )

    return response.text.strip()


# =========================================================
# CLEAN SQL
# =========================================================

def clean_sql(sql):

    sql = sql.strip()

    sql = re.sub(
        r"```sql",
        "",
        sql,
        flags=re.IGNORECASE
    )

    sql = sql.replace("```", "")

    sql = sql.strip()

    return sql.rstrip(";").strip()


# =========================================================
# SQL VALIDATION
# =========================================================

def validate_sql(sql):

    sql = clean_sql(sql)

    if not sql:

        return False, "SQL query is empty."

    if not re.match(
        r"^(SELECT|WITH)\b",
        sql,
        re.IGNORECASE
    ):

        return False, (
            "Only SELECT or WITH queries are allowed."
        )

    if ";" in sql:

        return False, (
            "Multiple SQL statements are not allowed."
        )

    dangerous_words = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "CREATE",
        "TRUNCATE",
        "ATTACH",
        "DETACH",
        "PRAGMA",
        "VACUUM"
    ]

    for word in dangerous_words:

        if re.search(
            rf"\b{word}\b",
            sql,
            re.IGNORECASE
        ):

            return False, (
                f"Unsafe SQL command detected: {word}"
            )

    if not re.search(
        r"\bCollege_Student\b",
        sql,
        re.IGNORECASE
    ):

        return False, (
            "College_Student table is required."
        )

    return True, sql


# =========================================================
# ASK GEMINI
# =========================================================

def ask_question(question):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

        return

    if not GEMINI_READY:

        st.error(
            "Gemini API key is not configured."
        )

        st.info(
            "Add GEMINI_API_KEY in "
            ".streamlit/secrets.toml"
        )

        return

    try:

        with st.spinner(
            "✨ Gemini is generating SQL..."
        ):

            sql = generate_sql(question)

        valid, cleaned_sql = validate_sql(sql)

        if not valid:

            st.error(
                cleaned_sql
            )

            return

        st.session_state.question = question

        st.session_state.sql = cleaned_sql

        st.session_state.result = None

        st.success(
            "SQL generated successfully."
        )

    except Exception as e:

        st.error(
            "Unable to generate SQL."
        )

        st.caption(str(e))


# =========================================================
# RUN QUERY
# =========================================================

def run_query():

    sql = st.session_state.sql

    if not sql:

        st.warning(
            "Generate SQL first."
        )

        return

    valid, checked_sql = validate_sql(sql)

    if not valid:

        st.error(
            checked_sql
        )

        return

    try:

        with st.spinner(
            "▶ Running SQL query..."
        ):

            df = execute_sql(
                checked_sql
            )

        st.session_state.result = df

        st.session_state.history.insert(
            0,
            {
                "question": st.session_state.question,
                "sql": checked_sql,
                "rows": len(df),
                "time": datetime.now().strftime(
                    "%d %b %Y, %I:%M %p"
                )
            }
        )

        st.session_state.history = (
            st.session_state.history[:20]
        )

        st.success(
            f"Query executed successfully — "
            f"{len(df)} rows found."
        )

    except Exception as e:

        st.error(
            "SQL execution failed."
        )

        st.caption(str(e))


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎓 StudentSQL AI")

    st.caption(
        "Natural Language to SQL"
    )

    st.divider()

    st.subheader("Navigation")

    if st.button(
        "🏠  Home",
        use_container_width=True
    ):

        st.session_state.page = "Home"
        st.rerun()

    if st.button(
        "💬  Ask AI",
        use_container_width=True
    ):

        st.session_state.page = "Ask AI"
        st.rerun()

    if st.button(
        "🗄️  Database Explorer",
        use_container_width=True
    ):

        st.session_state.page = "Database Explorer"
        st.rerun()

    if st.button(
        "🕘  Query History",
        use_container_width=True
    ):

        st.session_state.page = "Query History"
        st.rerun()

    if st.button(
        "📊  Analytics",
        use_container_width=True
    ):

        st.session_state.page = "Analytics"
        st.rerun()

    if st.button(
        "⚙️  Settings",
        use_container_width=True
    ):

        st.session_state.page = "Settings"
        st.rerun()

    st.divider()

    st.subheader("Database Info")

    if database_exists():

        st.success(
            "🟢 SQLite Connected"
        )

        st.write(
            "College_Student.db"
        )

    else:

        st.error(
            "🔴 Database not found"
        )

    st.divider()

    st.subheader("AI Status")

    if GEMINI_READY:

        st.success(
            "🟢 Gemini Ready"
        )

    else:

        st.warning(
            "🟡 Gemini Not Configured"
        )


# =========================================================
# TOP HEADER
# =========================================================

col1, col2 = st.columns(
    [4, 1]
)

with col1:

    st.title(
        "🎓 StudentSQL AI"
    )

    st.caption(
        "Natural Language to SQL for College Data"
    )

with col2:

    if database_exists():

        st.success(
            "🟢 SQLite Connected"
        )

    else:

        st.error(
            "🔴 SQLite Offline"
        )

st.divider()


# =========================================================
# HOME
# =========================================================

if st.session_state.page == "Home":

    st.header(
        "StudentSQL AI"
    )

    st.write(
        "Ask questions about your college student data "
        "in natural language and let Gemini convert "
        "them into SQL."
    )

    st.write("")

    # -----------------------------------------------------
    # STATISTICS
    # -----------------------------------------------------

    if database_exists():

        try:

            df = get_student_data()

            total_students = len(df)

            departments = df[
                "Department"
            ].nunique()

            average_cgpa = df[
                "CGPA"
            ].mean()

            highest_cgpa = df[
                "CGPA"
            ].max()

            c1, c2, c3, c4 = st.columns(4)

            with c1:

                st.metric(
                    "👨‍🎓 Total Students",
                    total_students
                )

            with c2:

                st.metric(
                    "🏢 Departments",
                    departments
                )

            with c3:

                st.metric(
                    "📈 Average CGPA",
                    f"{average_cgpa:.2f}"
                )

            with c4:

                st.metric(
                    "🏆 Highest CGPA",
                    f"{highest_cgpa:.2f}"
                )

        except Exception as e:

            st.error(
                f"Unable to load statistics: {e}"
            )


    st.write("")


    # -----------------------------------------------------
    # ASK SECTION
    # -----------------------------------------------------

    left, right = st.columns(
        [2.2, 1]
    )

    with left:

        st.subheader(
            "💬 Ask a Question"
        )

        st.caption(
            "Ask anything about your college student database."
        )

        question = st.text_area(
            "Your question",
            value=st.session_state.question,
            placeholder=(
                "Example: Show students with CGPA "
                "above 8 from CSE department"
            ),
            height=130
        )

        st.session_state.question = question

        b1, b2 = st.columns(
            [3, 1]
        )

        with b1:

            if st.button(
                "✨ Generate SQL",
                type="primary",
                use_container_width=True
            ):

                ask_question(
                    question
                )

        with b2:

            if st.button(
                "Clear",
                use_container_width=True
            ):

                st.session_state.question = ""
                st.session_state.sql = ""
                st.session_state.result = None

                st.rerun()


        # -------------------------------------------------
        # QUICK QUESTIONS
        # -------------------------------------------------

        st.write("")

        st.subheader(
            "⚡ Quick Questions"
        )

        q1, q2 = st.columns(2)

        with q1:

            if st.button(
                "How many students are there?",
                use_container_width=True
            ):

                ask_question(
                    "How many students are there?"
                )

            if st.button(
                "Show all CSE students",
                use_container_width=True
            ):

                ask_question(
                    "Show all CSE students"
                )

            if st.button(
                "Show top 10 students",
                use_container_width=True
            ):

                ask_question(
                    "Show top 10 students by CGPA"
                )

        with q2:

            if st.button(
                "Average CGPA by department",
                use_container_width=True
            ):

                ask_question(
                    "What is the average CGPA of each department?"
                )

            if st.button(
                "Students with CGPA above 8",
                use_container_width=True
            ):

                ask_question(
                    "Show students whose CGPA is above 8"
                )

            if st.button(
                "Male and female count",
                use_container_width=True
            ):

                ask_question(
                    "How many male and female students are there?"
                )


        # -------------------------------------------------
        # GENERATED SQL
        # -------------------------------------------------

        if st.session_state.sql:

            st.write("")

            st.subheader(
                "🔹 Generated SQL"
            )

            st.code(
                st.session_state.sql,
                language="sql"
            )

            if st.button(
                "▶ Run Query",
                type="primary",
                use_container_width=True
            ):

                run_query()


        # -------------------------------------------------
        # RESULTS
        # -------------------------------------------------

        if st.session_state.result is not None:

            result_df = (
                st.session_state.result
            )

            st.write("")

            st.subheader(
                "📋 Query Results"
            )

            r1, r2 = st.columns(2)

            with r1:

                st.metric(
                    "Rows",
                    len(result_df)
                )

            with r2:

                st.metric(
                    "Columns",
                    len(result_df.columns)
                )

            if result_df.empty:

                st.warning(
                    "No matching records found."
                )

            else:

                st.dataframe(
                    result_df,
                    use_container_width=True,
                    hide_index=True
                )

                csv = result_df.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    "⬇️ Download CSV",
                    csv,
                    "student_results.csv",
                    "text/csv",
                    use_container_width=True
                )


    # -----------------------------------------------------
    # AI ASSISTANT
    # -----------------------------------------------------

    with right:

        st.subheader(
            "✨ AI Assistant"
        )

        if GEMINI_READY:

            st.success(
                "🟢 Online"
            )

        else:

            st.warning(
                "🟡 API Not Configured"
            )

        st.write("")

        st.info(
            "Hello! I'm your StudentSQL AI Assistant."
        )

        st.write(
            "Ask me anything about your college data. "
            "I'll convert your question into SQL and "
            "help you understand the result."
        )

        st.divider()

        st.subheader(
            "🕘 Recent Queries"
        )

        if not st.session_state.history:

            st.caption(
                "No executed queries yet."
            )

        else:

            for item in st.session_state.history[:5]:

                st.write(
                    f"**{item['question']}**"
                )

                st.caption(
                    f"{item['time']} • "
                    f"{item['rows']} rows"
                )

                st.divider()


# =========================================================
# ASK AI PAGE
# =========================================================

elif st.session_state.page == "Ask AI":

    st.header(
        "💬 Ask AI"
    )

    st.write(
        "Ask questions about your student database "
        "using normal English."
    )

    question = st.text_area(
        "Your question",
        value=st.session_state.question,
        placeholder=(
            "Example: Which department has "
            "the highest average CGPA?"
        ),
        height=150
    )

    st.session_state.question = question

    if st.button(
        "✨ Generate SQL",
        type="primary",
        use_container_width=True
    ):

        ask_question(question)

    if st.session_state.sql:

        st.subheader(
            "🔹 Generated SQL"
        )

        st.code(
            st.session_state.sql,
            language="sql"
        )

        if st.button(
            "▶ Run Query",
            type="primary",
            use_container_width=True
        ):

            run_query()

    if st.session_state.result is not None:

        st.subheader(
            "📋 Results"
        )

        st.dataframe(
            st.session_state.result,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# DATABASE EXPLORER
# =========================================================

elif st.session_state.page == "Database Explorer":

    st.header(
        "🗄️ Database Explorer"
    )

    if not database_exists():

        st.error(
            "College_Student.db not found."
        )

    else:

        st.subheader(
            "📋 Table Structure"
        )

        info = get_table_info()

        st.dataframe(
            info,
            use_container_width=True,
            hide_index=True
        )

        st.write("")

        st.subheader(
            "👨‍🎓 Student Records"
        )

        df = get_student_data()

        search = st.text_input(
            "🔎 Search",
            placeholder=(
                "Search by name, department or gender..."
            )
        )

        if search:

            mask = df.astype(str).apply(
                lambda row:
                row.str.contains(
                    search,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )

            display_df = df[mask]

        else:

            display_df = df

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# QUERY HISTORY
# =========================================================

elif st.session_state.page == "Query History":

    st.header(
        "🕘 Query History"
    )

    if not st.session_state.history:

        st.info(
            "No query history available."
        )

    else:

        if st.button(
            "🗑️ Clear History"
        ):

            st.session_state.history = []

            st.rerun()

        for i, item in enumerate(
            st.session_state.history
        ):

            st.subheader(
                f"{i + 1}. {item['question']}"
            )

            st.caption(
                f"{item['time']} • "
                f"{item['rows']} rows"
            )

            st.code(
                item["sql"],
                language="sql"
            )

            st.divider()


# =========================================================
# ANALYTICS
# =========================================================

elif st.session_state.page == "Analytics":

    st.header(
        "📊 Analytics"
    )

    if not database_exists():

        st.error(
            "Database not found."
        )

    else:

        df = get_student_data()

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Total Students",
                len(df)
            )

        with c2:

            st.metric(
                "Average CGPA",
                f"{df['CGPA'].mean():.2f}"
            )

        with c3:

            st.metric(
                "Highest CGPA",
                f"{df['CGPA'].max():.2f}"
            )

        with c4:

            st.metric(
                "Lowest CGPA",
                f"{df['CGPA'].min():.2f}"
            )

        st.write("")

        st.subheader(
            "🏢 Students by Department"
        )

        department_count = (
            df["Department"]
            .value_counts()
            .sort_index()
        )

        st.bar_chart(
            department_count
        )

        st.subheader(
            "📈 Average CGPA by Department"
        )

        avg_cgpa = (
            df.groupby(
                "Department"
            )["CGPA"]
            .mean()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            avg_cgpa
        )

        st.subheader(
            "👥 Gender Distribution"
        )

        gender_count = (
            df["Gender"]
            .value_counts()
        )

        st.bar_chart(
            gender_count
        )


# =========================================================
# SETTINGS
# =========================================================

elif st.session_state.page == "Settings":

    st.header(
        "⚙️ Settings"
    )

    st.subheader(
        "🤖 Gemini API"
    )

    if GEMINI_READY:

        st.success(
            "🟢 Gemini API is configured."
        )

    else:

        st.warning(
            "🟡 Gemini API is not configured."
        )

        st.code(
            'GEMINI_API_KEY = "YOUR_API_KEY"',
            language="toml"
        )

    st.write("")

    st.subheader(
        "🗄️ Database"
    )

    if database_exists():

        st.success(
            "🟢 College_Student.db found."
        )

    else:

        st.error(
            "🔴 College_Student.db not found."
        )

    st.write("")

    st.subheader(
        "🔒 SQL Security"
    )

    st.success(
        "✅ Only SELECT / WITH queries"
    )

    st.success(
        "✅ INSERT blocked"
    )

    st.success(
        "✅ UPDATE blocked"
    )

    st.success(
        "✅ DELETE blocked"
    )

    st.success(
        "✅ DROP blocked"
    )

    st.success(
        "✅ Multiple SQL statements blocked"
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🎓 StudentSQL AI • SQLite + Gemini • "
    "Natural Language to SQL"
)