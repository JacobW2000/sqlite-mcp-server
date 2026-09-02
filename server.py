from fastmcp import FastMCP
from database import add_employee, update_salary, delete_employee, get_employee, highest_paid_employee, average_salary, total_employees, list_departments, employees_per_department, company_statistics, search_employee, all_employees

mcp = FastMCP("SQLite Database Server")

@mcp.tool(
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False
    }
)
def create_employee(name: str, department: str, salary: int):
    """Add a new employee to the database."""
    return add_employee(name, department, salary)

@mcp.tool(
    annotations={
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def change_salary(employee_id: int, new_salary: int):
    """Update an employee's salary using their unique employee ID."""
    return update_salary(employee_id, new_salary)

@mcp.tool(
    annotations={
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def remove_employee(employee_id: int):
    """Delete an employee from the database using their unique employee ID."""
    return delete_employee(employee_id)

@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def find_employee(employee_id: int):
    """Get an employee's information from the database by searching their unique employee ID."""
    return get_employee(employee_id)

@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def employee_search(name: str):
    """Search for employees by name. Returns all matching employees if multiple employees have the same name."""
    return search_employee(name)

@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def highest_salary():
    """Return the employee with the highest salary."""
    return highest_paid_employee()

@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def salary_average():
    """Calculate the average salary of all the employees."""
    return average_salary()

@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def employee_count():
    """Return the total number of employees in the database."""
    return total_employees()

@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def departments():
    """Return a list of all departments represented in the database."""
    return list_departments()

@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def department_count():
    """Return the total number of employees in each department."""
    return employees_per_department()

@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def company_stats():
    """Return a summary of the company's employee and salary statistics."""
    return company_statistics()

@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def list_employees():
    """Return all employees currently in the database."""
    return all_employees()

if __name__ == "__main__":
    mcp.run()