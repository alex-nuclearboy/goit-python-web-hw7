from connect_db import session
from models import Group, Student, Teacher, Discipline, Grade
from faker import Faker
import random
from datetime import datetime

# Pre-defined constants for the initial database seeding.
GROUPS = ['PyWeb20-1', 'PyWeb20-2', 'PyWeb20-3']
DISCIPLINES = [
    'Python Core',
    'Python Web Development',
    'Data Science',
    'Design Patterns',
    'Databases and SQL',
    'Artificial Intelligence',
    'Soft skills',
    'IT English'
]

NUMBER_STUDENTS = 50
NUMBER_TEACHERS = 5
NUMBER_GRADES = 20
MIN_GRADE = 1
MAX_GRADE = 5

faker = Faker()  # Creating a Faker object to generate fake data.


def generate_date():
    """
    Generates a random date within the current academic year.

    Returns:
        A random date as a datetime object within the academic year.
    """
    today = datetime.now()
    # If we passed September, the academic year starts this year
    if today.month > 9:
        start_date = datetime(today.year, 9, 1)
    else:  # Otherwise, the academic year started last September
        start_date = datetime(today.year - 1, 9, 1)

    return faker.date_between(start_date, today)


def create_groups():
    """
    Creates and adds group entities to the database based on predefined names.
    """
    for group_name in GROUPS:
        group_ = Group(name=group_name)
        session.add(group_)
    session.commit()


def create_students():
    """
    Creates student entities and assigns them to groups randomly.
    """
    groups = session.query(Group).all()  # Retrieve groups from the database.

    for _ in range(NUMBER_STUDENTS):
        student_ = Student(
            name=faker.name(),
            group_id=random.choice(groups).id
        )
        session.add(student_)
    session.commit()


def create_teachers():
    """
    Creates teachers and adds them to the database.
    """
    for _ in range(NUMBER_TEACHERS):
        teacher_ = Teacher(
            name=faker.name()
        )
        session.add(teacher_)
    session.commit()


# teachers = session.query(Teacher).all()


def create_disciplines():
    """
    Creates discipline entities and randomly distributes them among teachers.
    """
    # Retrieve all teachers from the database.
    teachers = session.query(Teacher).all()
    # Shuffle the list of disciplines.
    shuffled_disciplines = random.sample(DISCIPLINES, len(DISCIPLINES))

    for i, discipline_name in enumerate(shuffled_disciplines):
        # Determine the teacher index for this discipline.
        teacher_ix = i % len(teachers)
        discipline_ = Discipline(
            name=discipline_name,
            # Assign the discipline to a teacher.
            teacher_id=teachers[teacher_ix].id
        )
        session.add(discipline_)

    session.commit()


def award_grades():
    """
    Randomly awards grades to students for different disciplines.
    """
    # Retrieve all students and disciplines from the database.
    students = session.query(Student).all()
    disciplines = session.query(Discipline).all()
    for student in students:
        total_grades = random.randint(5, NUMBER_GRADES)
        for _ in range(total_grades):
            discipline = random.choice(disciplines)
            grade_ = Grade(
                student_id=student.id,
                discipline_id=discipline.id,
                grade=random.randint(MIN_GRADE, MAX_GRADE),
                grade_date=generate_date()
            )
            session.add(grade_)
    session.commit()


if __name__ == '__main__':
    create_groups()
    create_students()
    create_teachers()
    create_disciplines()
    award_grades()
    print("Database has been seeded.")
