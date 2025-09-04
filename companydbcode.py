import sqlite3

conn = sqlite3.connect("company2.db")
cursor = conn.cursor()

# Drop old tables if rerun
cursor.execute("DROP TABLE IF EXISTS employees")
cursor.execute("DROP TABLE IF EXISTS departments")
cursor.execute("DROP TABLE IF EXISTS salaries")

# Create tables
cursor.execute("""
CREATE TABLE departments (
    dept_id INTEGER PRIMARY KEY,
    dept_name TEXT
)
""")

cursor.execute("""
CREATE TABLE employees (
    emp_id INTEGER PRIMARY KEY,
    name TEXT,
    position TEXT,
    dept_id INTEGER,
    FOREIGN KEY(dept_id) REFERENCES departments(dept_id)
)
""")

cursor.execute("""
CREATE TABLE salaries (
    emp_id INTEGER,
    amount INTEGER,
    FOREIGN KEY(emp_id) REFERENCES employees(emp_id)
)
""")

# Insert data
departments = [
    (1, "HR"),
    (2, "Finance"),
    (3, "Engineering"),
    (4, "Sales")
]
cursor.executemany("INSERT INTO departments VALUES (?,?)", departments)

employees = [
    (1, "Alice", "Manager", 1),
    (2, "Bob", "Clerk", 1),
    (3, "Charlie", "Analyst", 2),
    (4, "David", "Clerk", 2),
    (5, "Eva", "Engineer", 3),
    (6, "Frank", "Engineer", 3),
    (7, "Grace", "Technician", 3),
    (8, "Hank", "Salesperson", 4),
    (9, "Ivy", "Salesperson", 4),
    (10, "Jack", "Manager", 4)
]
cursor.executemany("INSERT INTO employees VALUES (?,?,?,?)", employees)

salaries = [
    (1, 80000),
    (2, 35000),
    (3, 60000),
    (4, 30000),
    (5, 90000),
    (6, 85000),
    (7, 40000),
    (8, 45000),
    (9, 47000),
    (10, 95000)
]
cursor.executemany("INSERT INTO salaries VALUES (?,?)", salaries)

conn.commit()
conn.close()

print("company2.db created successfully!")