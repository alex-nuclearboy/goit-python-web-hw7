from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
import random

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

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    group_name = Column(String, unique=True)
    students = relationship("Student", backref="group")


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id'))


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    disciplines = relationship("Discipline", backref="teacher")


class Discipline(Base):
    __tablename__ = 'disciplines'
    id = Column(Integer, primary_key=True)
    discipline_name = Column(String, unique=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    discipline_id = Column(Integer, ForeignKey('disciplines.id'))
    grade = Column(Integer)
    grade_date = Column(Date)
    student = relationship("Student", backref="grades")
    discipline = relationship("Discipline", backref="grades")


# Connect to the database and create tables
engine = create_engine('sqlite:///university_database.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

faker = Faker()

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

# Add disciplines
for discipline in DISCIPLINES:
    discipline = Discipline(
        discipline_name=discipline,
        teacher_id=random.randint(1, NUMBER_TEACHERS)
    )
    session.add(discipline)

session.commit()

# Add students
for _ in range(NUMBER_STUDENTS):
    student = Student(
        full_name=faker.unique.name(),
        group_id=random.randint(1, len(GROUPS))
    )
    session.add(student)

session.commit()

# Add grades
for _ in range(NUMBER_STUDENTS * NUMBER_GRADES):
    grade = Grade(
        student_id=random.randint(1, NUMBER_STUDENTS),
        discipline_id=random.randint(1, len(DISCIPLINES)),
        grade=random.randint(1, 5),
        grade_date=faker.date_between(start_date="-1y", end_date="today")
    )
    session.add(grade)

session.commit()

session.close()
