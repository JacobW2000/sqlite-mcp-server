import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "employees.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn

def developer_run_query(sql):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(sql)

    rows = cursor.fetchall()
    results = [dict(row) for row in rows]

    conn.close()

    return results

def add_employee(name, department, salary):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO Employees (name, department, salary)
        VALUES (?, ?, ?)
        """,
        (name, department, salary)
    )

    conn.commit()
    conn.close()

    return {
        "message": f"{name} added successfully!"
    }

def update_salary(employee_id, new_salary):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE Employees
        SET salary = ?
        WHERE id = ?
        """,
        (new_salary, employee_id)
    )

    if cursor.rowcount == 0:
        conn.close()
        return {
            "error": f"No employee with ID #{employee_id} was found."
        }

    conn.commit()

    conn.close()

    return {
        "message": f"Employee #{employee_id}'s salary updated to ${new_salary:,}."
    }

def delete_employee(employee_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM Employees
        WHERE id = ?
        """,
        (employee_id,)
    )

    if cursor.rowcount == 0:
        conn.close()
        return {
            "error": f"No employee with ID #{employee_id} was found."
        }

    conn.commit()

    conn.close()

    return {
        "message": f"Employee #{employee_id} was removed successfully!"
    }

def get_employee(employee_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM Employees
        WHERE id = ?
        """,
        (employee_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return {
            "error": f"No employee with ID {employee_id} was found."
        }

    return dict(row)

def search_employee(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT *
    FROM Employees
    WHERE name = ?
    """,
    (name,)
    )

    rows = cursor.fetchall()

    employees = [dict(row) for row in rows]

    conn.close()

    if not employees:
        return {
            "error": f"No employee named '{name}' was found."
        }

    return employees

def highest_paid_employee():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT *
    FROM Employees
    ORDER BY salary DESC
    LIMIT 1;
    """,
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)

    return {
        "error": "No employees found."
    }

def average_salary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT AVG(salary) AS average_salary
    FROM Employees;
    """
    )

    row = cursor.fetchone()

    conn.close()

    if row["average_salary"] is None:
        return {
            "error": "No employees found."
        }

    return row["average_salary"]

def total_employees():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT COUNT(*) AS total
    FROM Employees;
    """
    )

    row = cursor.fetchone()

    conn.close()

    return row["total"]

def list_departments():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT DISTINCT department
    FROM Employees;
    """
    )

    rows = cursor.fetchall()

    conn.close()

    return [row["department"] for row in rows]

def employees_per_department():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT department, COUNT(*) AS employee_count
    FROM Employees
    GROUP BY department;
    """
    )

    rows = cursor.fetchall()

    conn.close()

    return {
        row["department"]: row["employee_count"]
        for row in rows
    }

def company_statistics():
    if total_employees() == 0:
        return {
            "message": "The company currently has no employees."
        }

    return {
        "total_employees": total_employees(),
        "average_salary": average_salary(),
        "departments": list_departments(),
        "department_counts": employees_per_department()
    }

def all_employees():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT *
    FROM Employees
    """
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]