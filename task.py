# Class diary
#
# Create program for handling lesson scores.
# Use python to handle student (highschool) class scores, and attendance.
# Make it possible to:
# - Get students total average score (average across classes)
# - get students average score in class
# - hold students name and surname
# - Count total attendance of student
#
# Please, use your imagination and create more functionalities.
# Your project should be able to handle entire school(s?).
# If you have enough courage and time, try storing (reading/writing)
# data in text files (YAML, JSON).
# If you have even more courage, try implementing user interface (might be text-like).
#
#Try to expand your implementation as best as you can. 
#Think of as many features as you can, and try implementing them.
#Make intelligent use of pythons syntactic sugar (overloading, iterators, generators, etc)
#Most of all: CREATE GOOD, RELIABLE, READABLE CODE.
#The goal of this task is for you to SHOW YOUR BEST python programming skills.
#Impress everyone with your skills, show off with your code.
#
#Your program must be runnable with command "python task.py".
#Show some usecases of your library in the code (print some things)
#
#When you are done upload this code to your github repository. 
#
#Delete these comments before commit!
#Good luck.
import logging
from typing import List, Callable


class Student:
    name: str

    def __init__(self, name: str):
        self.name = name


class Lesson:
    absent_students: list[int]
    student_grades: list[list[int]]

    def __init__(self, absent_students: list[int], students_count: int):
        self.absent_students = absent_students
        self.student_grades = [[] for _ in range(students_count)]

    def add_student_grade(self, student_index: int, grade: int):
        if len(self.student_grades) > student_index:
            self.student_grades[student_index].append(grade)
        else:
            logging.warning("No such student!")


class Subject:
    lessons: List[Lesson]
    name: str
    __students_count_getter: Callable[[], int]

    def __init__(self, name, __students_count_getter: Callable[[], int]):
        self.lessons = []
        self.name = name
        self.__students_count_getter = __students_count_getter

    def add_lesson(self, absent_students: list[int]):
        self.lessons.append(Lesson(absent_students, self.__students_count_getter()))

    def get_student_total_attendance(self, student_index: int):
        total_attendance = 0
        for lesson in self.lessons:
            total_attendance += 1 if student_index not in lesson.absent_students else 0
        return total_attendance

    def get_class_total_attendance(self):
        total_attendance = 0
        for lesson in self.lessons:
            total_attendance += self.__students_count_getter() - len(lesson.absent_students)
        return total_attendance

    def get_students_average_grade(self, student_index: int) -> float:
        grades_count = 0
        grades_sum = 0
        for lesson in self.lessons:
            grades_count += len(lesson.student_grades[student_index])
            grades_sum += sum(lesson.student_grades[student_index])

        return grades_sum / grades_count


class SchoolClass:
    code: str
    year: int
    subjects: List[Subject]
    students: List[Student]

    def __init__(self, code, year):
        self.code = code
        self.year = year

    def add_subject(self, name: str):
        self.subjects.append(Subject(name, lambda: len(self.students)))

    def add_student(self, name: str):
        self.students.append(Student(name))

    def get_student_average_grade(self, student_index: int):
        grades_sum = 0
        for subject in self.subjects:
            grades_sum += subject.get_students_average_grade(student_index)
        return grades_sum / len(self.subjects)

    def get_class_average_grade(self):
        grades_sum = 0
        for student_index in range(len(self.students)):
            grades_sum += self.get_student_average_grade(student_index)
        return grades_sum / len(self.students)

    def get_student_total_attendance(self, student_index: int):
        total_attendance = 0
        for subject in self.subjects:
            total_attendance += subject.get_student_total_attendance(student_index)
        return total_attendance

    def get_class_total_attendance(self):
        total_attendance = 0
        for subject in self.subjects:
            total_attendance += subject.get_class_total_attendance()
        return total_attendance


class School:
    classes: List[SchoolClass]

    def __init__(self):
        self.classes = []

    def check_if_class_with_year_and_code_exists(self, code: str, year: int):
        found_classes = [c for c in self.classes if c.year == year and c.code == code]
        if len(found_classes) != 0:
            return True
        return False

    def get_school_average_grade(self):
        grades_sum = 0
        for school_class in self.classes:
            grades_sum += school_class.get_class_average_grade()
        return grades_sum / len(self.classes)

    def add_class(self, code: str, year: int):
        if not self.check_if_class_with_year_and_code_exists(code, year):
            self.classes.append(SchoolClass(year, code))
        else:
            logging.warning("A class with such code and year exists, skipping")


if __name__ == '__main__':
    logging.info("I had no time to implement the CLI")
