# Dummy DB (CSV) Template

This directory contains CSV templates for a simple dummy database to support local testing and development. Populate these files with sample data as needed.

## Files

- roles.csv: Role definitions
- departments.csv: Departments and locations
- employees.csv: Employees with foreign keys to roles and departments

## Conventions

- Use lowercase snake_case column names.
- Keep id values unique within each file.
- Timestamps should be ISO 8601 (e.g., 2024-01-01T12:00:00Z).

## Minimal schema

- roles.csv: role_id,role_name,role_description
- departments.csv: department_id,department_name,location
- employees.csv: employee_id,first_name,last_name,email,hire_date,salary,role_id,department_id

You can add more CSV files or columns as your tests require.
