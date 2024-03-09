from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table

Base = declarative_base()

'''
Association table for the many-to-many relationship
between teachers and disciplines
'''
teacher_discipline = Table(
    'teacher_discipline',
    Base.metadata,
    Column('teacher_id', Integer, ForeignKey('teachers.id'), primary_key=True),
    Column('discipline_id', Integer, ForeignKey('disciplines.id'),
           primary_key=True)
)


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    students = relationship('Student', backref='group')

    def __str__(self):
        return self.name


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    group_id = Column(Integer, ForeignKey('groups.id'))
    grades = relationship('Grade', back_populates='student')

    def __str__(self):
        return self.name


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    disciplines = relationship('Discipline',
                               secondary=teacher_discipline,
                               back_populates='teachers')

    def __str__(self):
        return self.name


class Discipline(Base):
    __tablename__ = 'disciplines'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    teachers = relationship('Teacher',
                            secondary=teacher_discipline,
                            back_populates='disciplines')
    grades = relationship('Grade', back_populates='discipline')

    def __str__(self):
        return self.discipline_name


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    discipline_id = Column(Integer, ForeignKey('disciplines.id'))
    grade = Column(Integer)
    grade_date = Column(Date)
    student = relationship("Student", back_populates="grades")
    discipline = relationship("Discipline", back_populates="grades")
