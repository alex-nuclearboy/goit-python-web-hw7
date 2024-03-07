from models import session, Group, Student, Teacher, Discipline, Grade
from faker import Faker
import random
from datetime import datetime

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

faker = Faker()


def generate_date():
    '''
    Function for generating dates within an academic year
    '''
    # Generate academic year date range
    today = datetime.now()
    # If we passed June, the academic year starts this year in September
    if today.month > 6:
        start_date = datetime(today.year, 9, 1)
    else:  # Otherwise, the academic year started last September
        start_date = datetime(today.year - 1, 9, 1)

    return faker.date_between(start_date, today)


# Add groups
for group_name in GROUPS:
    group = Group(group_name=group_name)
    session.add(group)

# Add teachers
for _ in range(NUMBER_TEACHERS):
    teacher = Teacher(
        full_name=faker.unique.name()
    )
    session.add(teacher)

session.commit()

# Add disciplines
teachers = session.query(Teacher).all()

for discipline_name in DISCIPLINES:
    discipline = Discipline(
        discipline_name=discipline_name,
        teacher_id=random.choice(teachers).id)
    session.add(discipline)

session.commit()

# Add students
groups = session.query(Group).all()

for _ in range(NUMBER_STUDENTS):
    student = Student(
        full_name=faker.name(),
        group_id=random.choice(groups).id)
    session.add(student)

session.commit()

# Add grades
students = session.query(Student).all()
disciplines = session.query(Discipline).all()

for student in students:
    total_grades = random.randint(5, 20)
    for _ in range(total_grades):
        discipline = random.choice(disciplines)
        grade = Grade(
            student_id=student.id,
            discipline_id=discipline.id,
            grade=random.randint(1, 5),
            grade_date=generate_date()
        )
        session.add(grade)

session.commit()

session.close()

print("Database has been seeded.")
