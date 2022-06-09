from __future__ import annotations

import pandas as pd
from student_class import Student
from room_class import Room
from course_class import Course


def main() -> tuple[dict]:
    students = load_students("data/studenten_en_vakken.csv")
    rooms = load_rooms("data/zalen.csv")
    courses = load_courses("data/vakken.csv")

    return (students, rooms, courses)


def load_students(filename: str) -> dict:
    data = pd.read_csv(filename)

    students = {}

    for _, row in data.iterrows():
        last_name = row[0]
        first_name = row[1]
        student_num = row[2]
        courses = [row[3], row[4], row[5], row[6], row[7]]
        students[student_num] = Student(last_name, first_name, student_num, courses)

    return students


def load_rooms(filename: str) -> dict:
    data = pd.read_csv(filename)

    rooms = {}
    for _, row in data.iterrows():
        room_num = row[0]
        student_cap = row[1]
        rooms[room_num] = Room(room_num, student_cap)

    return rooms


def load_courses(filename: str) -> dict:
    data = pd.read_csv(filename)

    courses = {}

    for _, row in data.iterrows():
        course = row[0]
        lecture = row[1]
        seminar = row[2]
        max_stud_seminar = row[3]
        practica = row[4]
        max_stud_pract = row[5]
        expected = row[6]
        courses[course] = Course(
            course,
            lecture,
            seminar,
            max_stud_seminar,
            practica,
            max_stud_pract,
            expected,
        )

    return courses


if __name__ == "__main__":
    main()
