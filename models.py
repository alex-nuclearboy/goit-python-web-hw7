from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Base = declarative_base()

SQLALCHEMY_DATABASE_URL = 'sqlite:///university_database.db'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Connect to the database
# engine = create_engine('sqlite:///university_database.db')
Session = sessionmaker(bind=engine)
session = Session()


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


# Create tables
Base.metadata.create_all(engine)
