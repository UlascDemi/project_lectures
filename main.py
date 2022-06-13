from src.loader.loader import load_students, load_rooms, load_courses

import pandas as pd
import numpy as np
import random
from tabulate import tabulate

# TODO getters voor course schrijven - Brechje
# TODO getters voor room schrijven - Ulas
# TODO getters voor student schrijven - Justin

# TODO docstrings in loader_pandas schrijven

# TODO README

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIME_SLOTS = ["9:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", "17:00-19:00"]


def main():

    rooms = load_rooms("data/zalen.csv")
    courses = load_courses("data/vakken.csv")
    students = load_students("data/studenten_en_vakken.csv")

    # -----------------------Enroll all students------------------------------------------
    for student in students:
        course_names = student.get_students_courses()
        for course_name in course_names:
            courses[course_name].enroll(student)

    # -----------------------Create timetable, based on courses---------------------------
    courses_list = list(courses.values())
    courses_sorted = sorted(
        courses_list, key=lambda course: course.get_expected_students(), reverse=True
    )

    available_rooms = []

    for room in rooms.values():
        for day in range(len(DAYS)):
            for time_slot in range(4):
                available_rooms.append((room, day, time_slot))

    # Go through all courses
    for course in courses_sorted:
        while not schedule_course(course, available_rooms):
            schedule_course(course, available_rooms)

    print_2d_list(students[0].get_time_table(), f"Student {students[0]}")
    print_2d_list(students[16].get_time_table(), f"Student {students[16]}")


def schedule_course(course, available_rooms) -> bool:
    if (
        schedule_lecture(course, available_rooms)
        and schedule_seminar
        and schedule_practica
    ):
        return True

    return False


def schedule_lecture(course, available_rooms) -> bool:
    """
    ALGORITHM

    Args:
        rooms (_type_): _description_
        course (_type_): _description_
    """

    # Checks if lectures need to be given
    if course.n_lecture == 0:
        return True

    minimum_cap = course.get_expected_students()

    # Get all the rooms with enough capacity to fit all students
    choosable_rooms = [
        room for room in available_rooms if (room[0].get_capacity() >= minimum_cap)
    ]

    # If no rooms found, choose new day and time slot and try over
    if len(choosable_rooms) == 0:
        print("werk ik")
        return False

    for i in range(course.n_lecture):
        # Choose random time slot
        index = random.choice(range(len(choosable_rooms)))
        room_time_slot = choosable_rooms[index]

        # Remove time slot from list
        available_rooms.pop(index)

        # Unpack tuple
        room = room_time_slot[0]
        day = room_time_slot[1]
        time_slot = room_time_slot[2]

        # Get time tables
        course_time_table = course.get_time_table()
        room_time_table = room.get_time_table()

        # Update time tables
        course_time_table[day][time_slot] = room
        room_time_table[day][time_slot] = course

        # Update time tables for all students
        for student in course.get_enrol_students():
            student_time_table = student.get_time_table()

            student_time_table[day][time_slot].append((room, course))

    return True


def schedule_seminar():
    pass


def schedule_practica():
    pass


def is_colliding(room, day, timeslot) -> bool:
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


def print_2d_list(list, type) -> None:
    print(f"Timetable: {type}")
    printable_list = np.transpose(np.array(list, dtype=object))
    print(
        tabulate(printable_list, headers=DAYS, showindex=TIME_SLOTS, tablefmt="github")
    )


if __name__ == "__main__":
    main()
