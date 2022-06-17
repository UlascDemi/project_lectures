#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Created By  :
# Created Date:
# ---------------------------------------------------------------------------
from __future__ import annotations

from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room
from src.loader.loader import load_students, load_rooms, load_courses

import pandas as pd
import numpy as np
import random

from tabulate import tabulate
from copy import deepcopy

# TODO getters voor course schrijven - Brechje
# TODO getters voor room schrijven - Ulas
# TODO getters voor student schrijven - Justin

# TODO docstrings in loader_pandas schrijven

# TODO een check maken of rooms niet overlappen

# TODO README

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIME_SLOTS = ["9:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", "17:00-19:00"]


def main():

    rooms = load_rooms("data/zalen.csv")
    courses = load_courses("data/vakken.csv", "data/abbreviations.txt")
    students = load_students("data/studenten_en_vakken.csv")

    # -----------------------Enroll all students------------------------------------------
    for student in students:
        course_names = student.get_students_courses()
        for course_name in course_names:
            courses[course_name].enroll(student)

    courses_list = list(courses.values())
    courses_sorted = sorted(
        courses_list, key=lambda course: course.get_n_enrol_students(), reverse=True
    )

    # ----------------------Subdivide students into groups--------------------------------
    for course in courses_sorted:
        course.calc_seminars()
        course.calc_practica()

        course.subdivide_into_groups(
            course.get_groups_per_seminar(),
            course.get_stud_per_sem_group(),
            course.get_seminar_groups(),
        )

        course.subdivide_into_groups(
            course.get_groups_per_practicum(),
            course.get_stud_per_prac_group(),
            course.get_practicum_groups(),
        )

        # TODO hier moeten nu nog de practica ingedeeld worden
        # course.subdivide_into_groups(practica dingen)

    # -----------------------Create timetable, based on courses---------------------------
    available_rooms = []

    # Create a list of all available rooms, with all available time slots
    for room in rooms.values():
        for day in range(len(DAYS)):
            for time_slot in range(4):
                available_rooms.append((room, day, time_slot))

    # Schedule all courses
    for course in courses_sorted:
        schedule_course(course, available_rooms)

    print_2d_list(students[16])
    print_2d_list(rooms["C0.110"])


    print(f"\nTotal conflict count: {conflict_count(students)}")
    print(f"Total maluspoint count: {maluspoint_count(students, rooms)}")


def get_choosable_rooms(rooms: list[Room], min_capacity: int) -> list:
    """_summary_

    Args:
        rooms (list:[Room]): a list containing all room objects
        min_capacity (int): the minimum capacity the rooms need to have

    Returns:
        list: _description_
    """
    choosable_rooms = [
        room for room in rooms if (room[0].get_capacity() >= min_capacity)
    ]

    return choosable_rooms


def schedule_course(course: Course, available_rooms: list[Room]) -> bool:
    """_summary_

    Args:
        course (Course): _description_
        available_rooms (list[Room]): _description_

    Returns:
        bool: _description_
    """
    if (
        schedule_lecture(course, available_rooms)
        and schedule_seminar(course, available_rooms)
        and schedule_practicum(course, available_rooms)
    ):
        return True

    return False


def schedule_lecture(course: Course, available_rooms: list[Room]) -> bool:
    """_summary_

    Args:
        course (Course): _description_
        available_rooms (list[Room]): _description_

    Returns:
        bool: _description_
    """
    for _ in range(course.n_lecture):
        # Checks if lectures need to be given
        if course.n_lecture == 0:
            return True

        minimum_cap = course.get_n_enrol_students()

        # Get all the rooms with enough capacity to fit all students
        choosable_rooms = get_choosable_rooms(available_rooms, minimum_cap)

        # If no rooms found, Schedule couldnt be found
        if len(choosable_rooms) == 0:
            print(f"Couldnt schedule lecture: {course}")
            return False

        # Choose random time slot
        room_time_slot = random.choice(choosable_rooms)

        # Remove time slot from available room time slots list
        available_rooms.remove(room_time_slot)

        # Unpack tuple
        room = room_time_slot[0]
        day = room_time_slot[1]
        time_slot = room_time_slot[2]

        # Get time tables
        course_time_table = course.get_time_table()
        room_time_table = room.get_time_table()

        # Update time tables
        course_time_table[day][time_slot] = room
        room_time_table[day][time_slot] = course, course.get_enrol_students()

        # Update time tables for all students
        for student in course.get_enrol_students():
            student_time_table = student.get_time_table()

            student_time_table[day][time_slot].append((room, course, "Lec"))

    return True


def schedule_seminar(course: Course, available_rooms: list[Room]) -> bool:
    """_summary_

    Args:
        course (Course): _description_
        available_rooms (list[Room]): _description_

    Returns:
        bool: _description_
    """
    seminar_groups = course.get_seminar_groups()

    # If there are no seminar groups, return the function
    if len(seminar_groups) == 0:
        return True

    # Repeat scheduling for the amount of times seminar needs to be given
    for _ in range(course.get_n_seminar()):

        # Schedule invidual groups
        for group in seminar_groups:

            minimum_cap = len(group)
            choosable_rooms = get_choosable_rooms(available_rooms, minimum_cap)

            # If no choosable rooms, return file and print message
            if len(choosable_rooms) == 0:
                print(f"Couldnt schedule seminar: {course}")
                return False

            # Choose a time slot
            room_time_slot = random.choice(choosable_rooms)

            # Remove time slot from available room time slots list
            available_rooms.remove(room_time_slot)

            # Unpack time_slot tuple
            room = room_time_slot[0]
            day = room_time_slot[1]
            time_slot = room_time_slot[2]

            # Get time tables
            course_time_table = course.get_time_table()
            room_time_table = room.get_time_table()

            # Update time table
            course_time_table[day][time_slot] = room
            room_time_table[day][time_slot] = course, group

            # Update time table of the students
            for student in group:
                student_time_table = student.get_time_table()
                student_time_table[day][time_slot].append((room, course, "Sem"))

    return True


def schedule_practicum(course: Course, available_rooms: list[Room]) -> bool:
    """_summary_

    Args:
        course (Course): _description_
        available_rooms (list[Room]): _description_

    Returns:
        bool: _description_
    """
    practicum_groups = course.get_practicum_groups()

    # If there are no seminar groups, return the function
    if len(practicum_groups) == 0:
        return True

    # Repeat scheduling for the amount of times seminar needs to be given
    for _ in range(course.get_n_practicum()):

        # Schedule invidual groups
        for group in practicum_groups:

            minimum_cap = len(group)
            choosable_rooms = get_choosable_rooms(available_rooms, minimum_cap)

            # If no choosable rooms, return file and print message
            if len(choosable_rooms) == 0:
                print(f"Couldnt schedule practicum: {course}")
                return False

            # Choose a time slot
            room_time_slot = random.choice(choosable_rooms)

            # Remove time slot from available room time slots list
            available_rooms.remove(room_time_slot)

            # Unpack time_slot tuple
            room = room_time_slot[0]
            day = room_time_slot[1]
            time_slot = room_time_slot[2]

            # Get time tables
            course_time_table = course.get_time_table()
            room_time_table = room.get_time_table()

            # Update time tables
            course_time_table[day][time_slot] = room
            room_time_table[day][time_slot] = course, group

            # Update time tables of the students
            for student in group:
                student_time_table = student.get_time_table()
                student_time_table[day][time_slot].append((room, course, "Prac"))

    return True


def conflict_count(students: list[Student]) -> int:
    """_summary_

    Args:
        students (list[Student]): _description_

    Returns:
        int: _description_
    """
    conflict_count = 0

    # Go through every student
    for student in students:
        time_table = student.get_time_table()

        # Go through every time day and timeslot
        for day in time_table:
            for time_slot in day:

                # If the timeslot has more than 1 entry, count the excess amount
                if len(time_slot) > 1:
                    conflict_count += len(time_slot) - 1

    return conflict_count


# def oud_tussenuur_count(students: list[Student]) -> int:
#     tussen_uur_maluspunt = 0
#     for student in students:
#         for day in student.get_time_table():
#             for i, _ in enumerate(day[:-2]):
#                 if len(day[i]) != 0 and len(day[i + 1]) == 0 and len(day[i + 2]) != 0:
#                     tussen_uur_maluspunt += 1
#             for i, _ in enumerate(day[:-3]):
#                 if len(day[i]) != 0 and len(day[i + 1]) == 0 and len(day[i + 2]) == 0 and  len(day[i + 3]) != 0:
#                     tussen_uur_maluspunt += 3
#     # als we een 5de tijdslot hebben moet er een try and except in komen anders index out of bounce
#     return tussen_uur_maluspunt


def tussenuur_count(students: list[Student]) -> int:
    tussen_uur_maluspunt = 0

    for student in students:
        for day in student.get_time_table():
            activiteit = 0
            first_activity = None
            last_activity = None

            for i, time_slot in enumerate(day):
                if len(time_slot) != 0:
                    if activiteit == 0:
                        first_activity = i
                    activiteit += 1
                    last_activity = i

            if first_activity != last_activity:
                amount_activities = last_activity - first_activity + 1
                tussen_uren = amount_activities - activiteit

                if tussen_uren == 1:
                    tussen_uur_maluspunt += 1
                elif tussen_uren == 2:
                    tussen_uur_maluspunt += 3
                elif tussen_uren > 2:
                    print("ERROR")

    return tussen_uur_maluspunt
        
def big_room_count(rooms: dict[Room]):
    #FUNCTIE NIET AFGESCHREVEN!!!
    #GEEFT ERROR. WE WAREN ER HELEMAAL KLAAR MEE
    #WE PROBEERDE DE VALUE VAN VIJFDE TIJDSLOT TE KRIJGEN IN ROOMS
    
    maluspunten = 0

    room = rooms["C0.110"]
    time_table = room.get_time_table()

    for day in time_table:
        if day[4] != "-":
            maluspunten += 5

    return maluspunten
    

def capacity_count(rooms: list[Room]) -> int:
    excess_students = 0

    for room in rooms:
        for day in room.get_time_table():
            for time_slot in day:

                # Go to next time_slot if timeslot is not used
                if time_slot == "-":
                    continue
                
                # Compare the amount of students scheduled and the capacity
                students_in_room = len(time_slot[1])
                capacity = room.get_capacity()
                
                if students_in_room > room.get_capacity():
                    excess_students += students_in_room - capacity

    return excess_students


def maluspoint_count(students: list[Student], rooms: dict[Room]):
    conflicts = conflict_count(students)
    nieuw_tussenuren = tussenuur_count(students)
    capacity_conflict = capacity_count(rooms)
    laat_tijdslot = big_room_count(rooms)

    maluspoint = conflicts + nieuw_tussenuren + capacity_conflict + laat_tijdslot

    return maluspoint


def is_colliding(room: Room, day: int, timeslot: int) -> bool:
    """_summary_

    Args:
        room (_type_): _description_
        day (_type_): _description_
        timeslot (_type_): _description_

    Returns:
        bool: _description_
    """
    if room.get_time_table()[day][timeslot] == "-":
        return False
    else:
        return True


def print_2d_list(object_to_print) -> None:

    time_table = object_to_print.get_time_table()

    time_table_copy = deepcopy(time_table)

    if isinstance(object_to_print, Student):
        print(f"Timetable Student: {object_to_print}")

        for i, _ in enumerate(time_table_copy):
            for j, time_slot in enumerate(time_table_copy[i]):
                if len(time_slot) == 0:
                    time_table_copy[i][j] = "-"
                else:
                    time_table_copy[i][j] = ", ".join(map(str, time_slot))

    elif isinstance(object_to_print, Course):
        print(f"Timetable Course: {object_to_print}")
    else:
        print(f"Timetable Room: {object_to_print}")

    printable_list = np.transpose(np.array(time_table_copy, dtype=object))
    print(
        tabulate(printable_list, headers=DAYS, showindex=TIME_SLOTS, tablefmt="github")
    )


if __name__ == "__main__":
    main()
