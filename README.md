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

This project uses the `Faker` library to fill the database with fictitious but realistic-looking data. While the names of students and teachers are randomly generated to add variety, the names of the groups and the disciplines are already set within the program and don't change. 

Using the `seed.py` script, the database is seeded with this data. The script uses `SQLAlchemy` sessions for efficient data insertion, ensuring quick and effective database population.

The setup includes 50 students spread out over 3 fixed groups, with 5 teachers, 8 predefined disciplines, and each student getting up to 20 grades across all these disciplines.

## Queries

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

## Project Installation and Usage Guide

To set up and use this project, follow the steps below to clone the repository, set up the environment, and start interacting with the database.

#### Setting Up the Project

Clone the repository to the local machine and navigate to the project directory:

    git clone https://github.com/alex-nuclearboy/goit-python-web-hw7.git
    cd goit-python-web-hw7

Initialise a Poetry virtual environment for dependency management:

    poetry init

Import dependencies listed in requirements.txt. The command varies slightly depending on your operating system.

**On Unix/Linux:**

    poetry add $(cat requirements.txt | tr '\n' ' ')

**On Windows (PowerShell):**

    Get-Content requirements.txt | ForEach-Object { poetry add $_ }

Once dependencies are installed, activate the Poetry environment to ensure all commands run within this isolated environment.

    poetry shell

#### Database Setup and Interaction

Use Alembic to apply migrations and generate the database schema:

    alembic upgrade head

Populate the database tables with initial data using the provided seeding script:

    python3 seed.py  # for Unix/Linux

    py seed.py  # for Windows

Execute predefined queries to analyse the data:

    python3 my_select.py  # for Unix/Linux

    py my_select.py  # for Windows

## CLI for CRUD operation

This project also features a CLI program for CRUD operations with the database directly from the command line.

#### Command Structure:

- Use the `--action` command or its shorthand `-a` for CRUD operations.
- Use the `--model` command or `-m` to specify the model to operate on. 
- Use the `--name` command or `-n` to provide name for creating or updating a record.
- Use the `--id` command  to specify the ID of the record to update or remove.

**Supported Operations:** `create`, `list`, `update`, `remove`.

**Models:** `Group`, `Student`, `Teacher`, `Discipline`.

#### Examples:

- For Unix/Linux:

        python3 main.py --action create -m Teacher --name 'Boris Jonson' # Create a teacher
        python3 main.py --action list -m Teacher # List all teachers
        python3 main.py --action update -m Teacher --id 3 --name 'Andry Bezos' # Update a teacher with id=3
        python3 main.py --action remove -m Teacher --id 3 # Remove a teacher with id=3

- For Windows:

        py main.py --action create -m Teacher -n 'Boris Jonson' # Create a teacher
        py main.py --action list -m Teacher # List all teachers
        py main.py --action update -m Teacher --id 3 -n 'Andry Bezos' # Update a teacher with id=3
        py main.py --action remove -m Teacher --id 3 # Remove a teacher with id=3
