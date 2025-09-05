from flask import Flask, request, jsonify, render_template
import os
import sqlite3
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv() 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# ------------------- DB -------------------
def get_tables_and_columns(db_path):
    """Fetch all tables and their columns from the SQLite DB"""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        schema = {}
        for table_name, in tables:
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = [col[1] for col in cursor.fetchall()]
            schema[table_name] = columns

    return schema


def run_sql(db_path, sql_query):
    """Run SQL query on uploaded DB and return columns + rows"""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
        except Exception as e:
            columns, rows = [], [("Error", str(e))]

    return columns, rows



# ------------------- LLM -------------------
def get_sql_from_llm(schema, user_query):
    """Ask LLM to convert English question to SQL using the DB schema"""
    schema_str = "\n".join([
        f"{table}: {cols}".replace("{", "{{").replace("}", "}}") 
        for table, cols in schema.items()
    ])

    prompt_text = f"""
You are an expert in converting natural language questions into correct SQL queries.
You are given a SQLite database schema:

{schema_str}

Rules:
1. Only output ONE valid SQLite statement. Never produce more than one.
2. Do not include explanations, comments, markdown, or code fences.
3. Use only the table and column names from the schema.
4. Handle joins correctly when data is spread across multiple tables 
   (e.g. employees and their salaries).
5. Use correct aggregate functions: AVG, SUM, MIN, MAX, COUNT.
6. For "highest" or "lowest", use ORDER BY ... DESC/ASC with LIMIT 1.
7. Be case insensitive when matching text values (use LIKE if needed).
8. Always generate executable SQLite queries.

Now, convert this English question into exactly ONE SQL statement:
{{user_query}}
"""

    prompt = ChatPromptTemplate.from_template(prompt_text)

    llm = ChatGroq(
        groq_api_key=os.environ.get("GROQ_API_KEY"),
        model_name="llama3-8b-8192"
    )

    chain = prompt | llm | StrOutputParser()
    sql_query = chain.invoke({"user_query": user_query})
    return sql_query


# ------------------- Routes -------------------
@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/query-page")
def query_page():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_db():
    file = request.files["database"]
    if file:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        try:
            schema = get_tables_and_columns(filepath)
            return jsonify({
                "message": f"Database {file.filename} uploaded successfully!",
                "db_filename": file.filename,
                "schema": schema
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "No file uploaded"}), 400


@app.route("/query", methods=["POST"])
def query_db():
    data = request.json
    db_filename = data.get("db_filename")
    user_query = data.get("question")

    if not db_filename or not user_query:
        return jsonify({"error": "db_filename and question are required"}), 400

    db_path = os.path.join(app.config['UPLOAD_FOLDER'], db_filename)

    try:
        schema = get_tables_and_columns(db_path)
        sql_query = get_sql_from_llm(schema, user_query)
        columns, results = run_sql(db_path, sql_query)

        return jsonify({
            "sql_query": sql_query,
            "columns": columns,
            "results": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":

    app.run(debug=True)
