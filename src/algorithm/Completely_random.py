from __future__ import annotations

from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room

import random


def get_choosable_rooms(rooms: list[Room], min_capacity: int) -> list:
    """
    List of rooms that are still available after scheduling courses.

    Args:
        rooms (list:[Room]): a list containing all room objects
        min_capacity (int): the minimum capacity the rooms need to have

    Returns:
        list: available rooms
    """
    choosable_rooms = rooms

    return choosable_rooms


def random_schedule_course(course: Course, available_rooms: list[Room]) -> bool:
    """
    Schedules courses based on random choices.

    Args:
        course (Course): course object 
        available_rooms (list[Room]): list of rooms that can be chosen to schedule 

    Returns:
        bool: returns true if course is scheduled
    """
    if (
        schedule_lecture(course, available_rooms)
        and schedule_seminar(course, available_rooms)
        and schedule_practicum(course, available_rooms)
    ):
        return True

    return False


def schedule_lecture(course: Course, available_rooms: list[Room]) -> bool:
    """
    Randomly selects a room to schedule lectures.

    Args:
        course (Course): dictionairy with course objects
        available_rooms (list[Room]): list of room objects 

    Returns:
        bool: return true if lecture is scheduled
    """
    for _ in range(course.n_lecture):
        # Checks if lectures need to be given
        if course.n_lecture == 0:
            return True

        # Get all the rooms with enough capacity to fit all students
        choosable_rooms = available_rooms

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
    """
    Randomly selects a room to schedule seminars.

    Args:
        course (Course): dictionairy with course objects
        available_rooms (list[Room]): list of room objects 

    Returns:
        bool: returns true is seminar is scheduled 
    """
    seminar_groups = course.get_seminar_groups()

    # If there are no seminar groups, return the function
    if len(seminar_groups) == 0:
        return True

    # Repeat scheduling for the amount of times seminar needs to be given
    for _ in range(course.get_n_seminar()):

        # Schedule invidual groups
        for group in seminar_groups:

            choosable_rooms = available_rooms

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
    """
    Randomly slects a room to schedule practicals.

    Args:
        course (Course): dictionairy with course objects
        available_rooms (list[Room]): list of room objects 


    Returns:
        bool: return true if practical is scheduled 
    """
    practicum_groups = course.get_practicum_groups()

    # If there are no seminar groups, return the function
    if len(practicum_groups) == 0:
        return True

    # Repeat scheduling for the amount of times seminar needs to be given
    for _ in range(course.get_n_practicum()):

        # Schedule invidual groups
        for group in practicum_groups:

            
            choosable_rooms = available_rooms

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