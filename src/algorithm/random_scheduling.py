from __future__ import annotations

from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room

import random


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
