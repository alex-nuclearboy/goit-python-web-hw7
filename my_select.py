from sqlalchemy import func, desc, and_
from connect_db import session
from models import Group, Student, Grade, Discipline, Teacher


def select_1():
    """
    Find the top 5 students with the highest average grade across all subjects.
    """
    query = session.query(
        Student.name,
        func.round(func.avg(Grade.grade), 2).label('average_grade'))\
        .select_from(Grade)\
        .join(Student)\
        .group_by(Student.id)\
        .order_by(desc('average_grade'))\
        .limit(5)
    return query.all()


def select_2():
    """
    Find the student with the highest average grade in a specific subject.
    """
    discipline_id = 5  # Example discipline ID
    query = session.query(
        Discipline.name,
        Student.name,
        func.round(func.avg(Grade.grade), 2).label('average_grade'))\
        .select_from(Grade)\
        .join(Student)\
        .join(Discipline)\
        .filter(Discipline.id == discipline_id)\
        .group_by(Student.id)\
        .order_by(desc("average_grade"))\
        .limit(1)
    return query.all()


def select_3():
    """
    Find the average grade in groups for a specific subject.
    """
    discipline_id = 5  # Example discipline ID
    query = session.query(
        Discipline.name,
        Group.name,
        func.round(func.avg(Grade.grade), 2).label('average_grade'))\
        .select_from(Grade)\
        .join(Student)\
        .join(Discipline)\
        .join(Group)\
        .filter(Discipline.id == discipline_id)\
        .group_by(Discipline.id, Group.id)\
        .order_by(desc('average_grade'))
    return query.all()


def select_4():
    """
    Find the average grade across all grades.
    """
    query = session.query(
        func.round(func.avg(Grade.grade), 2).label('average_grade'))\
        .select_from(Grade)
    return query.scalar()


def select_5():
    """
    Find which courses a specific teacher teaches.
    """
    teacher_id = 1  # Example teacher ID
    query = session.query(
        Teacher.name,
        Discipline.name)\
        .select_from(Teacher)\
        .join(Discipline)\
        .filter(Teacher.id == teacher_id)
    return query.all()


def select_6():
    """
    Find a list of students in a specific group.
    """
    group_id = 2  # Example group ID
    query = session.query(
        Group.name,
        Student.name)\
        .select_from(Student)\
        .join(Group)\
        .filter(Group.id == group_id)\
        .order_by(Student.name)
    return query.all()


def select_7():
    """
    Find grades of students in a specific group for a subject.
    """
    discipline_id = 5  # Example discipline ID
    group_id = 1  # Example group ID
    query = session.query(
        Group.name,
        Discipline.name,
        Student.name,
        Grade.grade,
        Grade.grade_date)\
        .select_from(Student)\
        .join(Group)\
        .join(Grade)\
        .join(Discipline)\
        .filter(and_(Discipline.id == discipline_id, Group.id == group_id))\
        .order_by(Student.name, Grade.grade)
    return query.all()


def select_8():
    """
    Find the average grade given by a specific teacher across their subjects.
    """
    teacher_id = 3  # Example teacher ID
    query = session.query(
        Teacher.name,
        func.round(func.avg(Grade.grade), 2).label('average_grade'))\
        .select_from(Teacher)\
        .join(Discipline)\
        .join(Grade)\
        .filter(Teacher.id == teacher_id)\
        .group_by(Teacher.id)

    return query.all()


def select_9():
    """
    Find a list of courses attended by a specific student.
    """
    student_id = 10  # Example student ID
    query = session.query(
        Student.name,
        Discipline.name)\
        .select_from(Grade)\
        .join(Student)\
        .join(Discipline)\
        .filter(Student.id == student_id)\
        .group_by(Student.name, Discipline.id)

    return query.all()


def select_10():
    """
    Find a list of courses that a specific teacher teaches to a given student.
    """
    student_id = 15  # Example student ID
    teacher_id = 1  # Example teacher ID
    query = session.query(
        Student.name.label("student_name"),
        Teacher.name.label("teacher_name"),
        Discipline.name.label("discipline_name"))\
        .select_from(Grade)\
        .join(Student)\
        .join(Discipline)\
        .join(Teacher)\
        .filter(Student.id == student_id, Teacher.id == teacher_id)\
        .group_by(Student.id, Teacher.id, Discipline.id)

    return query.all()


def select_11():
    """
    Find the average grade that a given teacher gives to a particular student.
    """
    student_id = 25  # Example student ID
    teacher_id = 5   # Example teacher ID
    query = session.query(
        Teacher.name.label("teacher_name"),
        Student.name.label("student_name"),
        func.round(func.avg(Grade.grade), 2).label("average_grade"))\
        .select_from(Grade)\
        .join(Student)\
        .join(Discipline)\
        .join(Teacher)\
        .filter(Student.id == student_id, Teacher.id == teacher_id)\
        .group_by(Teacher.id, Student.id)

    return query.all()


def select_12():
    """
    Find the grades of students in a particular group for a given subject
    in the last class.
    """
    group_id = 2  # Example group ID
    discipline_id = 1  # Example discipline ID
    # Find the latest grade_date for the specified group and discipline
    latest_grade_date_subquery = session.query(
        Grade.student_id,
        func.max(Grade.grade_date).label('latest_grade_date'))\
        .select_from(Grade)\
        .join(Student)\
        .join(Group)\
        .join(Discipline)\
        .filter(Group.id == group_id, Discipline.id == discipline_id)\
        .group_by(Grade.student_id).subquery()

    # Use the subquery to find grades of students on the latest grade_date
    query = session.query(
        Group.name.label("group_name"),
        Discipline.name.label("discipline_name"),
        Student.name.label("student_name"),
        Grade.grade,
        latest_grade_date_subquery.c.latest_grade_date)\
        .select_from(Grade)\
        .join(Student)\
        .join(Group)\
        .join(Discipline)\
        .join(latest_grade_date_subquery)\
        .filter(
            Group.id == group_id,
            Discipline.id == discipline_id,
            Grade.grade_date == latest_grade_date_subquery.c.latest_grade_date
        )\
        .order_by(Group.id, Discipline.id, Student.name, Grade.grade_date)

    return query.all()


def all_selects():
    """
    Execute and print the results of all selection queries.
    """
    functions = [
        select_1, select_2, select_3,
        select_4, select_5, select_6,
        select_7, select_8, select_9,
        select_10, select_11, select_12]
    for i, select_function in enumerate(functions, start=1):
        print(f"\nSelect {i}: {select_function.__doc__}")
        result = select_function()
        if isinstance(result, list):
            for row in result:
                print(row)
        else:
            print(result)


if __name__ == "__main__":
    all_selects()
