import argparse
from sqlalchemy.orm import sessionmaker
from connect_db import engine
from models import Group, Student, Teacher, Discipline

# Create a session
SessionLocal = sessionmaker(bind=engine)

# Setup command-line argument parsing
# This CLI supports CRUD operations on the university database,
# allowing manipulation of Groups, Students, Teachers, and Disciplines.
parser = argparse.ArgumentParser(
    prog='UneversityDatabase',
    description="CLI for CRUD operations on the database.")
parser.add_argument("-a", "--action", choices=[
    "create", "list", "update", "remove"],
    help="The CRUD operation to perform.")
parser.add_argument("-m", "--model", choices=[
    "Group", "Student", "Teacher", "Discipline"],
    help="The model to perform operations on.")
parser.add_argument("--name", "-n",
                    help="Name for creating or updating a record.")
parser.add_argument("--id", type=int,
                    help="ID of the record to update or remove.")

args = parser.parse_args()


def create_record(session, model, name):
    """
    Create a new record in the database based on the model type.

    Parameters:
        session: The database session.
        model: The model type to create (Group, Student, Teacher, Discipline).
        name: The name of the record to create.
    """
    if model == "Student":
        record = Student(name=name)
    elif model == "Teacher":
        record = Teacher(name=name)
    elif model == "Group":
        record = Group(name=name)
    elif model == "Discipline":
        record = Discipline(name=name)

    session.add(record)
    session.commit()
    print(f"{model} '{name}' created successfully.")


def list_records(session, model):
    """
    List all records of a specific model in the database.

    Parameters:
        session: The database session.
        model: The model type to list (Group, Student, Teacher, Discipline).
    """
    if model == "Teacher":
        records = session.query(Teacher).all()
    elif model == "Group":
        records = session.query(Group).all()
    elif model == "Student":
        records = session.query(Student).all()
    elif model == "Discipline":
        records = session.query(Discipline).all()

    for record in records:
        print(record)


def update_record(session, model, record_id, name):
    """
    Update an existing record's name in the database.

    Parameters:
        session: The database session.
        model: The model type of the record to update.
        record_id: The ID of the record to update.
        name: The new name for the record.
    """
    if model == "Teacher":
        record = session.query(Teacher).filter(Teacher.id == record_id).first()
    elif model == "Group":
        record = session.query(Group).filter(Group.id == record_id).first()
    elif model == "Student":
        record = session.query(Student).filter(Student.id == record_id).first()
    elif model == "Discipline":
        record = session.query(Discipline).filter(
            Discipline.id == record_id).first()

    if record:
        record.name = name
        session.commit()
        print(f"{model} with id={record_id} updated successfully.")
    else:
        print(f"{model} with id={record_id} not found.")


def remove_record(session, model, record_id):
    """
    Remove a record from the database.

    Parameters:
        session: The database session.
        model: The model type of the record to remove.
        record_id: The ID of the record to remove.
    """
    if model == "Teacher":
        record = session.query(Teacher).filter(Teacher.id == record_id).first()
    elif model == "Group":
        record = session.query(Group).filter(Group.id == record_id).first()
    elif model == "Student":
        record = session.query(Student).filter(Student.id == record_id).first()
    elif model == "Discipline":
        record = session.query(Discipline).filter(
            Discipline.id == record_id).first()

    if record:
        session.delete(record)
        session.commit()
        print(f"{model} with id={record_id} removed successfully.")
    else:
        print(f"{model} with id={record_id} not found.")


def main():
    """
    Main function to parse arguments and perform the requested CRUD operation.
    """
    db = SessionLocal()

    if args.action == "create" and args.name:
        create_record(db, args.model, args.name)
    elif args.action == "list":
        list_records(db, args.model)
    elif args.action == "update" and args.id and args.name:
        update_record(db, args.model, args.id, args.name)
    elif args.action == "remove" and args.id:
        remove_record(db, args.model, args.id)

    db.close()


if __name__ == "__main__":
    main()
