# Programma dat studentenvakken inload
# Roep functie aan vanuit

import csv
from csv import DictReader
from classes import Student, Rooms, Course


def load_course_registration(filename):
    """
    Load function which loads information from course registration
    """

    # Read the information from the file and add to variables
    with open(filename, "r", encoding="utf-8", errors="ignore") as csv_file:
        reader = csv.DictReader(csv_file)

        students = {}
        # geeft info per student door aan de class student
        for row in reader:
            achternaam = row["Achternaam"]
            voornaam = row["Voornaam"]
            studentnumber = row["Stud.Nr."]
            course1 = row["Vak1"]
            course2 = row["Vak2"]
            course3 = row["Vak3"]
            course4 = row["Vak4"]
            course5 = row["Vak5"]
            students[studentnumber] = Student(
                achternaam,
                voornaam,
                studentnumber,
                course1,
                course2,
                course3,
                course4,
                course5,
            )


def load_rooms(filename):
    """
    Load function which loads information from rooms
    """
    with open(filename, "r") as csv_file:
        reader = csv.DictReader(csv_file)

        rooms = {}
        # slaat informatie over de zalen en capaciteit op
        for row in reader:
            roomnumber = row["Zaalnummber"]
            capacity = row["Max. capaciteit"]
            rooms[roomnumber] = Rooms(roomnumber, capacity)

        print(rooms)


def load_courses(filename):
    """
    Load function which loads information about courses.
    """
    with open(filename, "r") as csv_file:
        reader = csv.DictReader(csv_file)

        courses = {}
        # slaat informatie over de zalen en capaciteit op
        for row in reader:
            course = row["Vak"]
            hoorcollege = row["#Hoorcollege"]
            werkcollege = row["#Werkcollege"]
            max_students_werkcollege = row["Max. stud. Werkcollege"]
            practica = row["#Practica"]
            max_students_practica = row["Max. stud. Practicum"]
            verwacht = row["Verwacht"]
            courses[course] = Course(
                course,
                hoorcollege,
                werkcollege,
                max_students_werkcollege,
                practica,
                max_students_practica,
                verwacht,
            )

        print(courses)


load_course_registration("data/studenten_en_vakken.csv")
load_rooms("data/zalen.csv")
load_courses("data/vakken.csv")
