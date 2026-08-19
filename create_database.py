import sqlite3

# Create/Open the database file
conn = sqlite3.connect("employees.db")

cursor = conn.cursor()

# Create the Employees table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary INTEGER NOT NULL
)
""")

# Insert some sample data
employees = [
    ("Alice", "Engineering", 120000),
    ("Bob", "Marketing", 80000),
    ("Charlie", "Sales", 95000),
    ("David", "Engineering", 130000),
    ("Emma", "HR", 75000)
]

cursor.executemany(
    "INSERT INTO Employees (name, department, salary) VALUES (?, ?, ?)",
    employees
)

conn.commit()
conn.close()

print("Database created successfully!")