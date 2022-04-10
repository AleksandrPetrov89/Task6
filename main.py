from functools import total_ordering


def average_grades(grades):
    """ Средняя оценка одного человека

        (dict) -> str | float

        Находит среднее арифметическое всех оценок в словаре, имеющего структуру:
        {key1: [i1, i2, ...], key2: [j1,j2,...], ...}

        Если оценок нет - выводит соответствующее сообщение.
    """
    num = 0
    sum1 = 0
    for list1 in grades.values():
        sum1 += sum(list1)
        num += len(list1)
    if num == 0:
        return f'\nОценок нет!'
    else:
        return sum1 / num


@total_ordering
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_l(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and (course in self.courses_in_progress or self.finished_courses) and (
                course in lecturer.courses_attached):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return print('Ошибка оценки lecturer')

    def __str__(self):
        text = (f'\nИмя: {self.name} \nФамилия: {self.surname}'
                f'\nСредняя оценка за домашние задания: {average_grades(self.grades)}'
                f'\nКурсы в процессе изучения: {", ".join(self.courses_in_progress)}'
                f'\nЗавершенные курсы: {", ".join(self.finished_courses)}\n')
        return text

    def __lt__(self, other):
        if isinstance(other, Student):
            return average_grades(self.grades) < average_grades(other.grades)
        else:
            return 'Ошибка, один из объектов не относится к классу Student'

    def __eq__(self, other):
        if isinstance(other, Student):
            return average_grades(self.grades) == average_grades(other.grades)
        else:
            return 'Ошибка, один из объектов не относится к классу Student'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


@total_ordering
class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        text = (f'\nИмя: {self.name} \nФамилия: {self.surname}'
                f'\nСредняя оценка за лекции: {average_grades(self.grades)}\n')
        return text

    def __lt__(self, other):
        if isinstance(other, Lecturer):
            return average_grades(self.grades) < average_grades(other.grades)
        else:
            return 'Ошибка, один из объектов не относится к классу Lecturer'

    def __eq__(self, other):
        if isinstance(other, Lecturer):
            return average_grades(self.grades) == average_grades(other.grades)
        else:
            return 'Ошибка, один из объектов не относится к классу Lecturer'


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and (
                course in student.courses_in_progress or student.finished_courses):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return print('Ошибка оценки студента')

    def __str__(self):
        text = f'\nИмя: {self.name} \nФамилия: {self.surname}\n'
        return text


def average_grades_st(list_st, course):
    """ Средняя оценка по студентам в рамках указанного курса

        (list, str) -> str | float

        list_st - список, состоящий из объектов класса Student
        course - курс, в рамках которого считаем оценки

        Находит среднее арифметическое всех оценок за указанный курс у всех студентов из списка.
        Если в списке присутствует объект другого класса - он пропускается.
        Если по указанному курсу у студентов из списка нет оценок - выводит соответствующее сообщение.
    """
    sum1 = 0
    num = 0
    for student in list_st:
        if isinstance(student, Student) and course in student.grades:
            sum1 += sum(student.grades[course])
            num += len(student.grades[course])
    if num == 0:
        return f'По курсу {course} у указанных студентов нет оценок'
    else:
        return sum1 / num


def average_grades_lec(list_lec, course):
    """ Средняя оценка по лекторам в рамках указанного курса

        (list, str) -> str | float

        list_lec - список, состоящий из объектов класса Lecturer
        course - курс, в рамках которого считаем оценки

        Находит среднее арифметическое всех оценок за указанный курс у всех лекторов из списка.
        Если в списке присутствует объект другого класса - он пропускается.
        Если по указанному курсу у лекторов из списка нет оценок - выводит соответствующее сообщение.
    """
    sum1 = 0
    num = 0
    for lecturer in list_lec:
        if isinstance(lecturer, Lecturer) and course in lecturer.grades:
            sum1 += sum(lecturer.grades[course])
            num += len(lecturer.grades[course])
    if num == 0:
        return f'По курсу {course} у указанных лекторов нет оценок'
    else:
        return sum1 / num


student1 = Student('student1', 'student111', 'your_gender')
student1.courses_in_progress += ['Python']
student1.courses_in_progress += ['Git']
student1.finished_courses += ['Введение в программирование']

student2 = Student('student2', 'student222', 'your_gender')
student2.courses_in_progress += ['Python']
student2.finished_courses += ['Введение в программирование']

reviewer1 = Reviewer('reviewer1', 'reviewer11')
reviewer1.courses_attached += ['Python']
reviewer1.courses_attached += ['Git']
reviewer1.courses_attached += ['Введение в программирование']

reviewer2 = Reviewer('reviewer2', 'reviewer22')
reviewer2.courses_attached += ['Python']
reviewer2.courses_attached += ['Введение в программирование']

lecturer1 = Lecturer('lecturer1', 'lecturer11')
lecturer1.courses_attached += ['Python']
lecturer1.courses_attached += ['Git']
lecturer1.courses_attached += ['Введение в программирование']

lecturer2 = Lecturer('lecturer2', 'lecturer22')
lecturer2.courses_attached += ['Python']
lecturer2.courses_attached += ['Введение в программирование']

reviewer1.rate_hw(student1, 'Python', 8)
reviewer1.rate_hw(student2, 'Python', 9)
reviewer2.rate_hw(student1, 'Python', 9)
reviewer2.rate_hw(student2, 'Python', 8)
reviewer1.rate_hw(student1, 'Git', 10)
reviewer2.rate_hw(student1, 'Введение в программирование', 10)
reviewer2.rate_hw(student2, 'Введение в программирование', 10)

student1.rate_l(lecturer1, 'Python', 10)
student1.rate_l(lecturer2, 'Python', 9)
student2.rate_l(lecturer1, 'Python', 9)
student2.rate_l(lecturer2, 'Python', 10)

student1.rate_l(lecturer1, 'Git', 10)

student1.rate_l(lecturer1, 'Введение в программирование', 9)
student1.rate_l(lecturer2, 'Введение в программирование', 10)
student2.rate_l(lecturer1, 'Введение в программирование', 9)
student2.rate_l(lecturer2, 'Введение в программирование', 9)


# reviewer2.rate_hw(student2, 'Python', 10)
# Строка выше - для выравнивания средней оценки студентов

print(student1)
# print(student1.grades)
print(student2)
# print(student2.grades)
print(f'Оценки "{student1.name}" <= "{student2.name}"? - {student1 <= student2}')
print(f'Оценки "{student1.name}" >= "{student2.name}"? - {student1 >= student2}')
print(f'Оценки "{student1.name}" < "{student2.name}"? - {student1 < student2}')
print(f'Оценки "{student1.name}" > "{student2.name}"? - {student1 > student2}')
print(f'Оценки "{student1.name}" = "{student2.name}"? - {student1 == student2}')


# student1.rate_l(lecturer1, 'Git', 10)
# Строка выше - для выравнивания средней оценки лекторов

print(lecturer1)
# print(lecturer1.grades)
print(lecturer2)
# print(lecturer2.grades)
print(f'Оценки "{lecturer1.name}" <= "{lecturer2.name}"? - {lecturer1 <= lecturer2}')
print(f'Оценки "{lecturer1.name}" >= "{lecturer2.name}"? - {lecturer1 >= lecturer2}')
print(f'Оценки "{lecturer1.name}" < "{lecturer2.name}"? - {lecturer1 < lecturer2}')
print(f'Оценки "{lecturer1.name}" > "{lecturer2.name}"? - {lecturer1 > lecturer2}')
print(f'Оценки "{lecturer1.name}" = "{lecturer2.name}"? - {lecturer1 == lecturer2}')

print(reviewer1)
print(reviewer2)

students = [student1, student2]
print(average_grades_st(students, 'Введение в программирование'))
print(average_grades_st(students, 'Git'))
print(average_grades_st(students, 'Python'))

print()
lecturers = [lecturer1, lecturer2]
print(average_grades_lec(lecturers, 'Введение в программирование'))
print(average_grades_lec(lecturers, 'Git'))
print(average_grades_lec(lecturers, 'Python'))

