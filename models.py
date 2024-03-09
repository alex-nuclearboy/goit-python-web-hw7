from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    students = relationship('Student', back_populates='group')

    def __str__(self):
        return self.name


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"))
    group = relationship('Group', back_populates='students')
    grades = relationship('Grade', back_populates='student')

    def __str__(self):
        return self.name


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    disciplines = relationship('Discipline', back_populates='teacher')

    def __str__(self):
        return self.name


class Discipline(Base):
    __tablename__ = 'disciplines'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete="CASCADE"))
    teacher = relationship('Teacher', back_populates='disciplines')
    grades = relationship('Grade', back_populates='discipline')

    def __str__(self):
        return self.name


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    grade_date = Column(Date, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id', ondelete="CASCADE"))
    discipline_id = Column(
        Integer, ForeignKey('disciplines.id', ondelete="CASCADE"))
    student = relationship("Student", back_populates="grades")
    discipline = relationship("Discipline", back_populates="grades")

    def __str__(self):
        return f"{self.grade}, ({self.grade_date.strftime('%Y-%m-%d')})"
