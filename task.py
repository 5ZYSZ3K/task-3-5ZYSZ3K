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
import inspect
import json
import logging

logging.basicConfig(level=logging.INFO)


with open("data.json", "r") as file:
    school = json.load(file)


def add_class(code: str, year: int):
    if code not in school:
        school[code] = {"year": year, "students": [], "subjects": {}}
    else:
        raise ValueError("Such index already exists!")


def add_student(class_code: str, name: str):
    school[class_code]["students"].append(name)


def add_subject(class_code: str, name: str):
    if name not in school[class_code]["subjects"]:
        school[class_code]["subjects"][name] = []
    else:
        raise ValueError("Such index already exists!")


def add_lesson(class_code: str, subject_name: str):
    school[class_code]["subjects"][subject_name].append({
        "absent_students": [],
        "student_grades": [[] for _ in range(len(school[class_code]["students"]))]
    })


def add_absent_student_to_a_lesson(class_code: str, subject_name: str, lesson_index: int, absent_student: int):
    school[class_code]["subjects"][subject_name][lesson_index]['absent_students'].append(absent_student)


def add_students_grade(class_code: str, subject_name: str, lesson_id: int, student_index: int, grade: int):
    school[class_code]["subjects"][subject_name][lesson_id]["student_grades"][student_index].append(grade)


def get_students_subject_average_grade(class_code: str, subject_name: str, student_index: int):
    grades = [grade for lesson in school[class_code]['subjects'][subject_name]
              for grade in lesson["student_grades"][student_index]]
    return sum(grades)/len(grades)


def get_students_average_grade(class_code: str, student_index: int):
    grades = [get_students_subject_average_grade(class_code, subject_name, student_index)
              for subject_name in school[class_code]["subjects"].keys()]
    return sum(grades)/len(grades)


def get_students_attendance_per_subject(class_code: str, subject_name: str, student_index: int):
    attendance = [0 if student_index in lesson["absent_students"] else 1
                  for lesson in school[class_code]['subjects'][subject_name]]
    return sum(attendance)/len(attendance)


def get_students_total_attendance(class_code: str, student_index: int):
    attendance = [
        0 if student_index in lesson["absent_students"] else 1 for subject in school[class_code]["subjects"].values()
        for lesson in subject
    ]
    return sum(attendance)/len(attendance)


def get_class_total_attendance(class_code: str):
    current_attendance = 0
    total_attendance = 0
    class_size = len(school[class_code]["students"])
    for subject in school[class_code]["subjects"]:
        for lesson in subject:
            current_attendance += class_size - len(lesson["absent_students"])
            total_attendance += class_size
    return current_attendance / total_attendance


def get_class_average_grade(class_code: str):
    grades = [
        get_students_average_grade(class_code, student_index) for student_index in range(school[class_code]["students"])
    ]
    return sum(grades)/len(grades)


def get_school_average_grade():
    grades = [get_class_average_grade(class_code) for class_code in school.keys()]
    return sum(grades)/len(grades)


def print_students_of_a_class(code: str):
    logging.info("Students: " + str(school[code]['students']))


def print_subjects_of_a_class(code: str):
    logging.info("Subjects: " + str(list(school[code]['subjects'].keys())))


def get_school_total_attendance():
    current_attendance = 0
    total_attendance = 0
    for school_class in school.values():
        class_size = len(school_class["students"])
        for subject in school_class["subjects"]:
            for lesson in subject:
                current_attendance += class_size - len(lesson["absent_students"])
                total_attendance += class_size
    return current_attendance / total_attendance


def save_to_file():
    with open("data.json", "w") as file:
        json.dump(school, file, indent=2)


prompts_map = {
    "1": {
        "label": "Add a class to the school",
        "arguments_label": "Type in (with spaces between) class code and class year",
        "function": add_class
    },
    "2": {
        "label": "List classes",
        "arguments_label": None,
        "function": lambda: logging.info(
            "Classes: " + str([f"code: {code} year: {school_class['year']}" for code, school_class in school.items()])
        )
    },
    "3": {
        "label": "Add a student to a class",
        "arguments_label": "Type in (with spaces between) the class code and the name of a person",
        "function": add_student
    },
    "4": {
        "label": "List students of a class",
        "arguments_label": "Type in the class code",
        "function": print_students_of_a_class
    },
    "5": {
        "label": "Add a subject to a class",
        "arguments_label": "Type in (with spaces between) the class code and the name of a subject",
        "function": add_subject
    },
    "6": {
        "label": "List subjects from a class",
        "arguments_label": "Type in the class code",
        "function": print_subjects_of_a_class
    },
    "7": {
        "label": "Add a lesson to a subject",
        "arguments_label": "Type in (with spaces between) the class code and the name of a subject",
        "function": add_lesson
    },
    "8": {
        "label": "Add an absent student to a lesson",
        "arguments_label": "Type in (with spaces between) the class code, the name of a subject,"
                           " the lesson id and the absent student index",
        "function": add_absent_student_to_a_lesson
    },
    "9": {
        "label": "Add a grade to a student",
        "arguments_label": "Type in (with spaces between) the class code, the name of a subject,"
                           " the lesson id, the student index and the grade",
        "function": add_students_grade
    },
    "10": {
        "label": "Get students average grade for a subject",
        "arguments_label": "Type in (with spaces between) the class code, the name of a subject and the student index",
        "function": get_students_subject_average_grade
    },
    "11": {
        "label": "Get students average grade",
        "arguments_label": "Type in (with spaces between) the class code and the student index",
        "function": get_students_average_grade
    },
    "12": {
        "label": "Get students attendance per subject",
        "arguments_label": "Type in (with spaces between) the class code, the subject name and the student index",
        "function": get_students_attendance_per_subject
    },
    "13": {
        "label": "Get students total attendance",
        "arguments_label": "Type in (with spaces between) the class code and the student index",
        "function": get_students_total_attendance
    },
    "14": {
        "label": "Get class total attendance",
        "arguments_label": "Type in the class code",
        "function": get_class_total_attendance
    },
    "15": {
        "label": "Get class average grade",
        "arguments_label": "Type in the class code",
        "function": get_class_average_grade
    },
    "16": {
        "label": "Get school average grade",
        "arguments_label": None,
        "function": get_school_average_grade
    },
    "17": {
        "label": "Get school total attendance",
        "arguments_label": None,
        "function": get_school_total_attendance
    },
    "18": {
        "label": "Save to file",
        "arguments_label": None,
        "function": save_to_file
    },
}


if __name__ == '__main__':
    while True:
        logging.info("\n".join([f"{index}. {entry['label']}" for index, entry in prompts_map.items()]))
        entry1 = input()
        if entry1 in prompts_map.keys():
            if prompts_map[entry1]["arguments_label"] is None:
                prompts_map[entry1]["function"]()
            else:
                logging.info(prompts_map[entry1]["arguments_label"])
                args = []
                index = 0
                entry2 = input().split(" ")
                print(entry2)
                try:
                    for argument in inspect.signature(prompts_map[entry1]["function"]).parameters.values():
                        args.append(argument._annotation(entry2[index]))
                        index += 1
                    output = prompts_map[entry1]["function"](*args)
                    if output is not None:
                        logging.info(output)
                except (ValueError, KeyError) as e:
                    print(e)
                    logging.warning("An error occured")
