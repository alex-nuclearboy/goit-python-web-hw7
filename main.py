import argparse
from sqlalchemy.orm import sessionmaker
from models import engine, Teacher, Group

# Create a session
SessionLocal = sessionmaker(bind=engine)

# Setup argparse
parser = argparse.ArgumentParser(
    description="CLI for CRUD operations on the database.")
parser.add_argument("-a", "--action", choices=[
    "create", "list", "update", "remove"],
    help="The CRUD operation to perform.")
parser.add_argument("-m", "--model", choices=[
    "Teacher", "Group"], help="The model to perform operations on.")
parser.add_argument("--name", "-n",
                    help="Name for creating or updating a record.")
parser.add_argument("--id", type=int,
                    help="ID of the record to update or remove.")

args = parser.parse_args()


def create_record(session, model, name):
    if model == "Teacher":
        record = Teacher(full_name=name)
    elif model == "Group":
        record = Group(group_name=name)
    # Add other models as needed

    session.add(record)
    print("Attempting to commit changes to the database...")
    session.commit()
    print("Changes committed successfully.")
    print(f"{model} '{name}' created successfully.")


def list_records(session, model):
    if model == "Teacher":
        records = session.query(Teacher).all()
    elif model == "Group":
        records = session.query(Group).all()
    # Add other models as needed

    for record in records:
        print(record)


def update_record(session, model, record_id, name):
    if model == "Teacher":
        record = session.query(Teacher).filter(Teacher.id == record_id).first()
    elif model == "Group":
        record = session.query(Group).filter(Group.id == record_id).first()
    # Add other models as needed

    if record:
        record.name = name
        session.commit()
        print(f"{model} with id={record_id} updated successfully.")
    else:
        print(f"{model} with id={record_id} not found.")


def remove_record(session, model, record_id):
    if model == "Teacher":
        record = session.query(Teacher).filter(Teacher.id == record_id).first()
    elif model == "Group":
        record = session.query(Group).filter(Group.id == record_id).first()
    # Add other models as needed

    if record:
        session.delete(record)
        session.commit()
        print(f"{model} with id={record_id} removed successfully.")
    else:
        print(f"{model} with id={record_id} not found.")


def main():
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
