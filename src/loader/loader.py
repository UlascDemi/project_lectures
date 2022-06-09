#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Created By  :
# Created Date: 31-05-2022
# ---------------------------------------------------------------------------
"""
"""

# Programma dat studentenvakken inload
# Roep functie aan vanuit

import csv
from csv import DictReader
from classes import Student, Room, Course


def load_course_registration(filename):
    """
    Load function which loads information from course registration
    """

    # Read the information from the file and add to variables
    with open(filename, "r", encoding="utf-8", errors="ignore") as csv_file:
        reader = DictReader(csv_file)

        students = {}
        # geeft info per student door aan de class student
        for row in reader:
            last_name = row["Achternaam"]
            first_name = row["Voornaam"]
            student_num = row["Stud.Nr."]
            courses = [row["Vak1"], row["Vak2"], row["Vak3"], row["Vak4"], row["Vak5"]]
            students[student_num] = Student(last_name, first_name, student_num, courses)


def load_rooms(filename):
    """
    Load function which loads information from rooms
    """
    with open(filename, mode="r", encoding="utf-8-sig", errors="ignore") as csv_file:
        reader = DictReader(csv_file)

        rooms = {}
        # slaat informatie over de zalen en capaciteit op
        for row in reader:
            roomnumber = row["Zaalnummber"]
            capacity = row["Max. capaciteit"]
            rooms[roomnumber] = Room(roomnumber, capacity)


def load_courses(filename):
    """
    Load function which loads information about courses.
    """
    with open(filename, "r") as csv_file:
        reader = DictReader(csv_file)

        courses = {}
        # slaat informatie over de zalen en capaciteit op
        for row in reader:
            course = row["Vak"]
            lecture = row["#Hoorcolleges"]
            seminar = row["#Werkcolleges"]
            max_stud_seminar = row["Max. stud. Werkcollege"]
            practica = row["#Practica"]
            max_stud_pract = row["Max. stud. Practicum"]
            expected = row["Verwacht"]
            courses[course] = Course(
                course,
                lecture,
                seminar,
                max_stud_seminar,
                practica,
                max_stud_pract,
                expected,
            )


load_course_registration("data/studenten_en_vakken.csv")
load_rooms("data/zalen.csv")
load_courses("data/vakken.csv")
