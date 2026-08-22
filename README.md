# Employee Database MCP Server

A small Python project that lets Claude Desktop interact with a SQLite employee database through the Model Context Protocol (MCP).

I built this project to learn how AI assistants can use external tools to retrieve and modify structured data.

## What it does

The server gives Claude a set of tools for working with employee data. For example, Claude can:

- Add an employee
- Find an employee by ID
- Search for employees by name
- List all employees
- Update an employee's salary
- Remove an employee
- Find the highest-paid employee
- Calculate the average salary
- List company departments
- Count employees by department
- Get overall company statistics

Because the tools are exposed through MCP, I can ask Claude questions in normal language instead of writing SQL queries myself.

## How it works

The project is split into three main parts:

```text
Claude Desktop
      |
      | MCP
      v
   server.py
      |
      v
  database.py
      |
      v
   SQLite
```

server.py exposes the database functions as MCP tools.

database.py handles the SQLite database operations.

## Technologies

- Python
- SQLite
- MCP / FastMCP
- pytest
- Git / GitHub

## Testing

This project includes 11 pytest tests covering database operations and employee queries.

Tests are run with:

```bash
python -m pytest tests/test_database.py
```