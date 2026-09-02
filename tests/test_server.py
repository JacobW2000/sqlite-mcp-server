import sqlite3

import pytest


@pytest.fixture
def test_db(monkeypatch, tmp_path):
    """
    Create an isolated temporary database for each test.

    This prevents the tests from modifying the real employees.db file.
    """
    db_path = tmp_path / "test_employees.db"

    def get_test_connection():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # Make all database functions use the temporary database.
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


def test_create_employee(test_db):
    from server import create_employee, find_employee

    result = create_employee("Alice", "Engineering", 90000)

    assert "successfully" in result["message"]

    employee = find_employee(1)

    assert employee["name"] == "Alice"
    assert employee["department"] == "Engineering"
    assert employee["salary"] == 90000


def test_change_salary(test_db):
    from server import create_employee, change_salary, find_employee

    create_employee("Bob", "Sales", 65000)

    result = change_salary(1, 75000)

    assert "updated" in result["message"]

    employee = find_employee(1)

    assert employee["salary"] == 75000


def test_remove_employee(test_db):
    from server import create_employee, remove_employee, find_employee

    create_employee("Charlie", "Marketing", 70000)

    result = remove_employee(1)

    assert "removed successfully" in result["message"]

    employee = find_employee(1)

    assert "error" in employee


def test_find_employee(test_db):
    from server import create_employee, find_employee

    create_employee("David", "HR", 55000)

    result = find_employee(1)

    assert result["id"] == 1
    assert result["name"] == "David"
    assert result["department"] == "HR"
    assert result["salary"] == 55000


def test_employee_search(test_db):
    from server import create_employee, employee_search

    create_employee("Alex", "Engineering", 90000)
    create_employee("Alex", "Sales", 65000)

    result = employee_search("Alex")

    assert len(result) == 2
    assert result[0]["name"] == "Alex"
    assert result[1]["name"] == "Alex"


def test_highest_salary(test_db):
    from server import create_employee, highest_salary

    create_employee("Alice", "Engineering", 90000)
    create_employee("Bob", "Sales", 65000)
    create_employee("Charlie", "Marketing", 110000)

    result = highest_salary()

    assert result["name"] == "Charlie"
    assert result["salary"] == 110000


def test_salary_average(test_db):
    from server import create_employee, salary_average

    create_employee("Alice", "Engineering", 80000)
    create_employee("Bob", "Sales", 75000)
    create_employee("Charlie", "Marketing", 70000)

    result = salary_average()

    assert result == 75000


def test_employee_count(test_db):
    from server import create_employee, employee_count

    create_employee("Alice", "Engineering", 90000)
    create_employee("Bob", "Sales", 65000)
    create_employee("Charlie", "Marketing", 110000)

    result = employee_count()

    assert result == 3


def test_departments(test_db):
    from server import create_employee, departments

    create_employee("Alice", "Engineering", 90000)
    create_employee("Bob", "Sales", 65000)
    create_employee("Charlie", "Marketing", 110000)

    result = departments()

    assert "Engineering" in result
    assert "Sales" in result
    assert "Marketing" in result
    assert len(result) == 3


def test_department_count(test_db):
    from server import create_employee, department_count

    create_employee("Alice", "Engineering", 90000)
    create_employee("Bob", "Engineering", 65000)
    create_employee("Charlie", "Marketing", 110000)

    result = department_count()

    assert result["Engineering"] == 2
    assert result["Marketing"] == 1


def test_company_stats(test_db):
    from server import create_employee, company_stats

    create_employee("Alice", "Engineering", 90000)
    create_employee("Bob", "Engineering", 80000)
    create_employee("Charlie", "Sales", 70000)

    result = company_stats()

    assert result["total_employees"] == 3
    assert result["average_salary"] == 80000
    assert "Engineering" in result["departments"]
    assert "Sales" in result["departments"]
    assert result["department_counts"]["Engineering"] == 2
    assert result["department_counts"]["Sales"] == 1


def test_list_employees(test_db):
    from server import create_employee, list_employees

    create_employee("Alice", "Engineering", 90000)
    create_employee("Bob", "Sales", 65000)
    create_employee("Charlie", "Marketing", 110000)

    result = list_employees()

    assert len(result) == 3

    assert result[0]["name"] == "Alice"
    assert result[1]["name"] == "Bob"
    assert result[2]["name"] == "Charlie"
