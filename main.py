from src.loader.loader import load_students, load_rooms, load_courses

import pandas as pd

# TODO getters voor course schrijven - Brechje
# TODO getters voor room schrijven - Ulas
# TODO getters voor student schrijven - Justin

# TODO docstrings in loader_pandas schrijven

# TODO README

# TODO moeten een functie schrijven die kijkt naar hoe veel en waar conflicts zijn. Een conflict is bijvoorbeeld "student moet op twee plekken tegelijk zijn"


def main():

    rooms = load_rooms("data/zalen.csv")
    courses = load_courses("data/vakken.csv")
    students = load_students("data/studenten_en_vakken.csv")

    # Enroll all students to their respective courses
    for student in students:
        course_names = student.get_students_courses()
        for course_name in course_names:
            courses[course_name].enroll(student)


if __name__ == "__main__":
    main()
