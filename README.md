# 🗄️ NL2SQL

**Ask questions in plain English. Get executable SQL.**

NL2SQL is a web application that converts natural language questions into **valid SQLite queries** and runs them directly on a user-provided database.

The project focuses on one core problem: *how do you reliably translate human intent into correct, executable SQL when the schema is unknown beforehand?*

Rather than hard-coding table logic, NL2SQL dynamically inspects the uploaded database, builds a schema-aware prompt, and lets an LLM reason about joins, aggregates, and filters in real time.

---

## ✨ What this project does well

* Works with **any SQLite database** uploaded at runtime
* Generates **single, executable SQL statements** (no explanations, no markdown)
* Handles joins, aggregates, and ordering based purely on schema inspection
* Keeps the system simple, debuggable, and transparent

This is not a toy chatbot that prints SQL-like text. The generated queries are actually executed against the database and returned as structured results.

---

## 🧩 Core Features

### 🗂️ Dynamic Schema Extraction

The app inspects the uploaded SQLite database to discover tables and columns automatically.

### 🧠 Schema-Aware Prompting

The LLM is given a strict, rule-based prompt that:

* limits output to a single SQL statement
* enforces valid SQLite syntax
* prevents hallucinated tables or columns

### ⚙️ Executable Queries

Generated SQL is run directly on the database and returned as rows and columns, not just text.

### 🌐 Simple Web Interface

A clean Flask-based UI allows users to:

* upload a database
* ask questions in plain English
* view both the generated SQL and the query results

---

## 🛠 Tech Stack

* **Python**
* **Flask** – backend and routing
* **SQLite** – database engine
* **LangChain** – prompt orchestration
* **Groq API** – fast LLM inference
* **LLaMA 3.1** – language model for NL → SQL reasoning

---

## 🔍 How it works (high level)

1. User uploads a SQLite database
2. The app extracts table and column information
3. A schema-aware prompt is constructed with strict rules
4. The LLM converts the natural language question into SQL
5. The SQL is executed and results are returned to the UI

---

## ▶️ Running the project locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/nl2sql.git
cd nl2sql
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

### 4. (Optional) Create a sample database

A helper script is included to generate a demo SQLite database:

```bash
python companydbcode.py
```

This creates `company2.db`, which can be uploaded and queried immediately.

### 5. Start the application

```bash
python app.py
```

Then open:

```
http://127.0.0.1:5000
```

## 🌱 Why this project exists

NL2SQL was built to explore:

* schema-aware LLM reasoning
* prompt constraints as a safety mechanism
* the boundary between natural language flexibility and deterministic systems

It treats SQL generation as a **systems problem**, not a prompt engineering trick.

---

If you’re interested in NL → SQL systems, database tooling, or applied LLM reasoning, feel free to explore the code or adapt the ideas for your own projects.
