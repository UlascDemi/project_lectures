from matplotlib.style import available
from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room
from src.loader.loader import load_students, load_rooms, load_courses

import pandas as pd
import numpy as np
import random
from tabulate import tabulate

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

    print_2d_list(students[16])

    print(f"\nConflict count: {conflict_count(students)}")


def schedule_course(course, available_rooms) -> bool:
    if (
        schedule_lecture(course, available_rooms)
        and schedule_seminar
        and schedule_practica
    ):
        return True

    return False


def schedule_lecture(course, available_rooms) -> bool:
    """_summary_

    Args:
        course (_type_): _description_
        available_rooms (_type_): _description_

    Returns:
        bool: _description_
    """
    for i in range(course.n_lecture):
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
            print("werk ik")  # moet later eruit
            return False

        # Choose random time slot
        room_time_slot = random.choice(choosable_rooms)

        # Remove time slot from list
        # TODO, maak beter search method (is nu linear time O(n))
        for j, time_slot in enumerate(available_rooms):
            if time_slot == room_time_slot:
                available_rooms.pop(j)

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


def conflict_count(students) -> int:
    """
    _summary_

    Args:
        students (_type_): _description_

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


def print_2d_list(object_to_print) -> None:

    list_to_print = object_to_print.get_time_table()
    object_type = type(object_to_print)

    # # BUG type vinden doet kut
    # print(isinstance(object_type, Student))
    # print(object_type)
    # print(type(Student))

    if object_type == type(Student):
        print(f"Timetable: Student {object_to_print}")
    elif object_type == type(Course):
        print(f"Timetable: Course {object_to_print}")
    else:
        print(f"Timetable: Room {object_to_print}")

    printable_list = np.transpose(np.array(list_to_print, dtype=object))
    print(
        tabulate(printable_list, headers=DAYS, showindex=TIME_SLOTS, tablefmt="github")
    )


if __name__ == "__main__":
    main()
