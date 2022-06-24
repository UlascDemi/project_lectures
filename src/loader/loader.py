from __future__ import annotations

import pandas as pd
import numpy as np

from src.classes import Student, Room, Course


def load_students(filename: str) -> list[Student]:
    """
    Loads in the data of all students and make objects of the Student class. 

    Args:
        filename (str): name of csv-file containing the data

    Returns:
        list[Student]: list of student objects
    """
    # Read data from csv file
    data = pd.read_csv(filename)

    # List of student objects
    students = []

    # Loop over the rows with the information per student and create a student object per 
    # student. This will be added to the list of students.
    for _, row in data.iterrows():
        last_name = row[0]
        first_name = row[1]
        student_num = row[2]
        courses = [course for course in row[3:8] if course is not np.NaN]
        students.append(Student(last_name, first_name, student_num, courses))

    return students


def load_rooms(filename: str) -> dict[Room]:
    """
    Loads in the data of all rooms and make objects of the Room class.

    Args:
        filename (str): name of csv-file containing the data

    Returns:
        dict[Room]: dictionary with as key the roomnumber and value the maximum capacity
    """
    # Read data from csv file
    data = pd.read_csv(filename)

    # Dictionary of room objects
    rooms = {}

    # Loop over the information per room and create a room object per room. This will be
    # added to the dictonary of rooms.
    for _, row in data.iterrows():
        room_num = row[0]
        student_cap = row[1]
        rooms[room_num] = Room(room_num, student_cap)

    return rooms


def load_courses(filename: str, abbreviations: str) -> dict[Course]:
    """
    Loads in the data of all courses and make objects of the Course class.

    Args:
        filename (str): name of csv-file containing the data of the courses
        abbreviations (str): name of csv-file containing the abbreviation of the course name

    Returns:
        dict[Course]: dictionary with course name as keys
    """
    # Read data for the courses from a csv file
    data = pd.read_csv(filename)

    # Read data for the abbreviations from a csv file
    abbr = pd.read_csv(abbreviations)

    # Creates a dictonary with courses as keys and abbreviations as value
    abbr_dict = dict(zip(abbr["course"], abbr["abbreviation"]))

    # Dictionary with course objects
    courses = {}

    # Loop over the information per course and create a course object per course. This will be
    # added to the dictonary of courses.
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
            abbr_dict[course],
            lecture,
            seminar,
            max_stud_seminar,
            practica,
            max_stud_pract,
            expected,
        )

    return courses
