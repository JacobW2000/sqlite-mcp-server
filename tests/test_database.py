import sqlite3
import pytest

@pytest.fixture
def test_db(monkeypatch, tmp_path):
    db_path = tmp_path / "test_employees.db"

    def get_test_connection():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    monkeypatch.setattr("database.get_connection", get_test_connection)

    conn = get_test_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE Employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        salary INTEGER NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()

    yield

def test_add_employee(test_db):
    from database import add_employee

    result = add_employee("Test Person", "Testing", 50000)

    assert "successfully" in result["message"]

def test_search_employees(test_db):
    from database import add_employee, search_employee

    add_employee("Alice", "Engineering", 90000)

    result = search_employee("Alice")

    assert len(result) == 1
    assert result[0]["name"] == "Alice"
    assert result[0]["department"] == "Engineering"
    assert result[0]["salary"] == 90000

def test_get_employee(test_db):
    from database import add_employee, get_employee,search_employee

    add_employee("Bob", "Sales", 65000)

    employees = search_employee("Bob")
    employee_id = employees[0]["id"]

    result = get_employee(employee_id)

    assert result["id"] == employee_id
    assert result["name"] == "Bob"
    assert result["department"] == "Sales"
    assert result["salary"] == 65000

def test_update_salary(test_db):
    from database import add_employee, get_employee, update_salary, search_employee

    add_employee("Charlie", "Marketing", 60000)

    employee = search_employee("Charlie")
    employee_id = employee[0]["id"]

    update_salary(employee_id, 75000)

    result = get_employee(employee_id)

    assert result["salary"] == 75000

def test_delete_employee(test_db):
    from database import add_employee, delete_employee, search_employee

    add_employee("David", "HR", 55000)

    employee = search_employee("David")
    employee_id = employee[0]["id"]

    delete_employee(employee_id)

    result = search_employee("David")

    assert "error" in result

def test_highest_paid_employee(test_db):
    from database import add_employee, highest_paid_employee

    add_employee("Alice", "Engineering", 90000)
    add_employee("Bob", "Sales", 65000)
    add_employee("Charlie", "Marketing", 110000)

    result = highest_paid_employee()

    assert result["name"] == "Charlie"
    assert result["salary"] == 110000

def test_average_salary(test_db):
    from database import add_employee, average_salary

    add_employee("Alice", "Engineering", 80000)
    add_employee("Bob", "Sales", 75000)
    add_employee("Charlie", "Marketing", 70000)

    result = average_salary()

    assert result == 75000

def test_total_employees(test_db):
    from database import add_employee, total_employees

    add_employee("Alice", "Engineering", 90000)
    add_employee("Bob", "Sales", 65000)
    add_employee("Charlie", "Marketing", 110000)

    result = total_employees()

    assert result == 3

def test_list_departments(test_db):
    from database import add_employee, list_departments

    add_employee("Alice", "Engineering", 90000)
    add_employee("Bob", "Sales", 65000)
    add_employee("Charlie", "Marketing", 110000)

    result = list_departments()

    assert "Engineering" in result
    assert "Sales" in result
    assert "Marketing" in result
    assert len(result) == 3

def test_employees_per_department(test_db):
    from database import add_employee, employees_per_department

    add_employee("Alice", "Engineering", 90000)
    add_employee("Bob", "Engineering", 65000)
    add_employee("Charlie", "Marketing", 110000)

    result = employees_per_department()

    assert result["Engineering"] == 2
    assert result["Marketing"] == 1

def test_company_statistics(test_db):
    from database import (
    add_employee,
    company_statistics
    )

    add_employee("Alice", "Engineering", 90000)
    add_employee("Bob", "Engineering", 80000)
    add_employee("Charlie", "Sales", 70000)

    result = company_statistics()

    assert result["total_employees"] == 3
    assert result["average_salary"] == 80000
    assert "Engineering" in result["departments"]
    assert "Sales" in result["departments"]
    assert result["department_counts"]["Engineering"] == 2
    assert result["department_counts"]["Sales"] == 1

def test_all_employees(test_db):
    from database import add_employee, all_employees

    add_employee("Alice", "Engineering", 90000)
    add_employee("Bob", "Sales", 65000)
    add_employee("Charlie", "Marketing", 110000)

    result = all_employees()

    assert len(result) == 3

    assert result[0]["name"] == "Alice"
    assert result[1]["name"] == "Bob"
    assert result[2]["name"] == "Charlie"