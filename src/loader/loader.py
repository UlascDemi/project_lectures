from __future__ import annotations

import pandas as pd
import numpy as np

from src.classes import Student, Room, Course


def load_students(filename: str) -> list:
    """_summary_

    Args:
        data (pd.DataFrame): _description_

    Returns:
        dict: _description_
    """
    data = pd.read_csv(filename)
    students = []

    for _, row in data.iterrows():
        last_name = row[0]
        first_name = row[1]
        student_num = row[2]
        courses = [course for course in row[3:8] if course is not np.NaN]
        students.append(Student(last_name, first_name, student_num, courses))

    return students


def load_rooms(filename: str) -> list:
    """_summary_

    Args:
        data (pd.DataFrame): _description_

    Returns:
        dict: _description_
    """

    data = pd.read_csv(filename)

    rooms = []

    for _, row in data.iterrows():
        room_num = row[0]
        student_cap = row[1]
        rooms.append(Room(room_num, student_cap))

    return rooms


def load_courses(filename: str) -> dict:
    """_summary_

    Args:
        data (pd.DataFrame): _description_

    Returns:
        dict: _description_
    """
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
