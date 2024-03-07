from sqlalchemy import func
from models import session, Student, Grade, Discipline, Teacher, Group


def select_1():
    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    query = session.query(
        Student.full_name,
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    ).join(Grade).group_by(Student.id)\
        .order_by(func.avg(Grade.grade).desc())\
        .limit(5)
    return query.all()


def select_2():
    # Знайти студента із найвищим середнім балом з певного предмета.
    discipline_id = 1  # Приклад ID предмета
    query = session.query(
        Discipline.discipline_name,
        Student.full_name,
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    ).select_from(Student).join(Grade).join(Discipline).\
        filter(Discipline.id == discipline_id).group_by(Student.id).\
        order_by(func.avg(Grade.grade).desc()).first()
    return query


def select_3():
    # Знайти середній бал у групах з певного предмета.
    discipline_id = 5  # Приклад ID предмета
    query = session.query(
        Discipline.discipline_name,
        Group.group_name,
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    ).join(Grade).join(Student).join(Group)\
        .filter(Discipline.id == discipline_id)\
        .group_by(Group.id).order_by(func.avg(Grade.grade).desc())
    return query.all()


def select_4():
    # Знайти середній бал на потоці (по всій таблиці оцінок).
    query = session.query(
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    )
    return query.scalar()


def select_5():
    # Знайти які курси читає певний викладач.
    teacher_id = 5  # Приклад ID викладача
    query = session.query(
        Teacher.full_name,
        Discipline.discipline_name
    ).join(Discipline).filter(Teacher.id == teacher_id)
    return query.all()


def select_6():
    # Знайти список студентів у певній групі.
    group_id = 2  # Приклад ID групи
    query = session.query(
        Group.group_name,
        Student.full_name
    ).join(Student).filter(Group.id == group_id)
    return query.all()


def select_7():
    # Знайти оцінки студентів у окремій групі з певного предмета.
    discipline_id = 5  # Приклад ID предмета
    group_id = 1  # Приклад ID групи
    query = session.query(
        Discipline.discipline_name,
        Group.group_name,
        Student.full_name,
        Grade.grade,
        Grade.grade_date
    ).select_from(Grade)\
        .join(Student)\
        .join(Group)\
        .join(Discipline)\
        .filter(Discipline.id == discipline_id, Group.id == group_id)
    return query.all()


def select_8():
    # Знайти середній бал, який ставить певний викладач зі своїх предметів.
    teacher_id = 1  # Приклад ID викладача
    query = session.query(
        Teacher.full_name,
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    ).select_from(Teacher)\
        .join(Discipline, Teacher.id == Discipline.teacher_id)\
        .join(Grade, Discipline.id == Grade.discipline_id)\
        .filter(Teacher.id == teacher_id)

    # Якщо очікується один результат, краще використати метод one_or_none()
    result = query.one_or_none()

    # Перевірка, чи результат існує, і повернення відформатованого результату
    if result:
        return f'{result[0]} - Average Grade: {result[1]}'
    else:
        return 'No data found'


def select_9():
    # Знайти список курсів, які відвідує певний студент.
    student_id = 10  # Приклад ID студента
    query = session.query(
        Student.full_name,
        Discipline.discipline_name
    ).select_from(Student)\
        .join(Grade, Student.id == Grade.student_id)\
        .join(Discipline, Grade.discipline_id == Discipline.id)\
        .filter(Student.id == student_id)\
        .distinct()

    return query.all()


def select_10():
    # Find a list of courses that a specific teacher teaches
    # to a specific student.
    student_id = 15  # Example student ID
    teacher_id = 1  # Example teacher ID
    query = session.query(
        Student.full_name,
        Teacher.full_name,
        Discipline.discipline_name
    ).select_from(Student)\
        .join(Grade, Student.id == Grade.student_id)\
        .join(Discipline, Grade.discipline_id == Discipline.id)\
        .join(Teacher, Discipline.teacher_id == Teacher.id)\
        .filter(Student.id == student_id, Teacher.id == teacher_id)\
        .distinct()

    return query.all()


def select_11():
    # Find the average grade that a given teacher gives
    # to a particular student.
    student_id = 25  # Example student ID
    teacher_id = 5   # Example teacher ID
    query = session.query(
        Teacher.full_name,
        Student.full_name,
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    ).select_from(Grade)\
        .join(Student, Grade.student_id == Student.id)\
        .join(Discipline, Grade.discipline_id == Discipline.id)\
        .join(Teacher, Discipline.teacher_id == Teacher.id)\
        .filter(Student.id == student_id, Teacher.id == teacher_id)\
        .group_by(Student.id, Teacher.id)

    return query.all()


def select_12():
    # Find the grades of students in a particular group
    # for a given subject in the last class.
    group_id = 3  # Example group ID
    discipline_id = 1  # Example discipline ID
    query = session.query(
        Group.group_name,
        Discipline.discipline_name,
        Student.full_name,
        Grade.grade,
        func.max(Grade.grade_date).label('date_of_last_grade')
    ).select_from(Grade)\
        .join(Student, Grade.student_id == Student.id)\
        .join(Group, Student.group_id == Group.id)\
        .join(Discipline, Grade.discipline_id == Discipline.id)\
        .filter(Group.id == group_id, Discipline.id == discipline_id)\
        .group_by(Student.id)\
        .order_by(Student.full_name)

    return query.all()


# Приклад виклику функції
if __name__ == "__main__":
    result = select_12()
    print(result)
