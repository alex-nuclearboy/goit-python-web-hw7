# GoIT Database Management Project

This project implements a simplified database schema designed for educational management purposes. It models the relationships between groups, students, teachers, disciplines (courses), and grades to practice database design, automated data generation, and query execution for various data retrieval tasks.

## Database Schema Overview

The schema is structured into the following tables to accurately represent the educational model:

- **Groups Table:** Lists the available student groups.
- **Students Table:** Details student identities with first and last names.
- **Teachers Table:** Stores details of teachers.
- **Disciplines Table:** Lists disciplines along with the respective teacher for each discipline.
- **Grades Table:** Records the grades students receive in various disciplines, noting the award date.

## Database Migrations

For database schema evolution, the project uses `alembic`. This tool facilitates version-controlled schema migrations, ensuring smooth updates and modifications.

## Data Generation and Seeding

Data generation leverages the `Faker` library, creating fictitious but realistic data for students and teachers. Group and discipline names are predefined. The `seed.py` script, using `SQLAlchemy` sessions, seeds the database efficiently with 50 students across 3 groups, 5 teachers, 8 disciplines, and assigns up to 20 grades per student.

## Project Installation and Usage Guide

To set up and use this project, follow the steps below to clone the repository, set up the environment, and start interacting with the database.

#### Setting Up the Project

Clone the repository and navigate to its directory:
```bash
git clone https://github.com/alex-nuclearboy/goit-python-web-hw7.git
cd goit-python-web-hw7
```
Activate the Poetry environment to ensure all commands run within this isolated environment:
```bash
poetry shell
```
#### Database Setup

Generate the database schema with `Alembic`:
```bash
alembic upgrade head
```

Populate the database tables with data using the provided seeding script.

- **Unix/Linux/macOS:**
```bash
python3 seed.py
```

- **Windows:**
```powershell
py seed.py
```

#### Database Queries

The `my_select.py` script is provided for executing various queries to retrieve information, such as:

- Identifying the top 5 students by average grade across all disciplines.
- Finding the student with the highest average grade in a specific discipline.
- Calculating average grades within groups for a specific discipline.
- Determining the overall average grade across all grades recorded.
- Listing disciplines taught by a specific teacher.
- Retrieving a list of students within a particular group.
- Finding grades of students in a specific group for a particular discipline.
- Calculating the average grade awarded by a specific teacher.
- Listing disciplines a student is enrolled in.
- Identifying disciplines taught to a specific student by a specific teacher.
- Calculating the average grade a teacher awards to a specific student.
- Finding grades awarded in the last class for a discipline within a specific group.

To execute these queries, use:

- **Unix/Linux/macOS:**
```bash
python3 my_select.py
```

- **Windows:**
```powershell
py my_select.py
```

## CLI for CRUD operation

The project includes a CLI program for direct CRUD operations on the database.

#### Command Structure:

- Perform CRUD operations using `--action` or `-a`.
- Specify the model with `--model` or `-m`.
- Provide a name with `--name` or `-n` for creating or updating a record.
- Specify a record's ID with `--id` to update or remove it.

**Supported Operations:** `create`, `list`, `update`, `remove`.

**Models:** `Group`, `Student`, `Teacher`, `Discipline`.

#### Examples:

- **Unix/Linux/macOS:**
```bash
python3 main.py --action create -m Teacher --name 'Boris Jonson' # Create a teacher
python3 main.py --action list -m Teacher # List all teachers
python3 main.py --action update -m Teacher --id 3 --name 'Andry Bezos' # Update a teacher with id=3
python3 main.py --action remove -m Teacher --id 3 # Remove a teacher with id=3
```

- **Windows:**
```powershell
py main.py --action create -m Teacher -n 'Boris Jonson' # Create a teacher
py main.py --action list -m Teacher # List all teachers
py main.py --action update -m Teacher --id 3 -n 'Andry Bezos' # Update a teacher with id=3
py main.py --action remove -m Teacher --id 3 # Remove a teacher with id=3
```
