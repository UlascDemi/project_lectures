from __future__ import annotations

from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room

import random


def get_choosable_rooms(
    room_time_slots: list[tuple[Room, int, int]], min_capacity: int
) -> list:
    """
    Returns a list containing all room time slots that are available and have enough
    capacity.
    This function expects a list with room time slots and an integer representing the
    minimum capacity amount. The room time slot is in the format of a tuple containing
    three elements: (Room, day, time_slot). Where Room is a Room object and the day and
    time_slot are represented by an int. In this case (Room1, 0, 0) would be room 1 on
    monday with the first time slot.
    The function returns a list in the same format as the input list with the room time
    slots that have enough capacity.

    Args:
        rooms (list[tuple[Room, int, int]]): a list with all available room_time_slots
        min_capacity (int): the minimum capacity to filter the rooms on

    Returns:
        list: a list containing the room time slots where the rooms have sufficient capacity
    """
    choosable_rooms = [
        room_time_slot
        for room_time_slot in room_time_slots
        if (room_time_slot[0].get_capacity() >= min_capacity)
    ]

    return choosable_rooms


def schedule_course(course: Course, available_rooms: list[Room]) -> bool:
    """
    This function schedules the all lectures, seminars and practica of course.
    The rooms and time slots are randomly chosen. If the course was already
    scheduled in, the course in unscheduled and scheduled again. If all
    activities of the course are scheduled succesfully, True is returned.
    If one of them fails, False is returned.

    Args:
        course (Course): the course that needs to be scheduled
        available_rooms (list[Room]): a list of all available room time slots

    Returns:
        bool: returns True if schedule was succesful, False if not
    """
    if is_scheduled(course):
        un_schedule(course, available_rooms)

    if (
        schedule_lecture(course, available_rooms)
        and schedule_seminar(course, available_rooms)
        and schedule_practicum(course, available_rooms)
    ):
        return True

    return False


def is_scheduled(course: Course) -> bool:
    """
    Checks if the course is already scheduled.
    
    Args:
        course (Course): a course object of the Course class

    Returns:
        bool: returns True if course is already planned in, False if not
    
    """
    time_table = course.get_time_table()

    for day in time_table:
        for time_slot in day:
            if time_slot != "-":
                return True


def un_schedule(course: Course, available_rooms: list) -> None:
    """
    Unschedules all lectures, seminars and practicals.  
    
    Args:
        course (Course): a course object of the Course class
        
    """
    time_table = course.get_time_table()

    students = course.get_enrol_students()
    
    # Go through each time slot of the timetable
    for i, day in enumerate(time_table):
        for j, time_slot in enumerate(day):
            # If time_slot is filled in, unschedul
            if time_slot != "-":
                for student in students:
                    student_time_slots = student.get_time_table()[i][j]
                    for k, (room_object, course_object, type) in enumerate(
                        student_time_slots
                    ):
                        if room_object == time_slot and course_object == course:
                            student_time_slots.pop(k)
                time_slot.get_time_table()[i][j] = "-"

                available_rooms.append((time_slot, i, j))
                time_table[i][j] = "-"


def schedule_lecture(course: Course, available_rooms: list[Room]) -> bool:
    """
    Schedules all lectures needed to be given for the given Course. These
    are all randomly scheduled.

    Args:
        course (Course): Course to be scheduled
        available_rooms (list[Room]): The available room time slots

    Returns:
        bool: True if lectures have been scheduled, False if not
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
        course_time_table[day][time_slot] = room, course.get_enrol_students()
        room_time_table[day][time_slot] = course, course.get_enrol_students()

        # Update time tables for all students
        for student in course.get_enrol_students():
            student_time_table = student.get_time_table()

            student_time_table[day][time_slot].append((room, course, "Lec"))

    return True


def schedule_seminar(course: Course, available_rooms: list[Room]) -> bool:
    """
    Schedules all seminars needed to be given for the given Course. These
    are all randomly scheduled.

    Args:
        course (Course): Course to be scheduled
        available_rooms (list[Room]): The available room time slots

    Returns:
        bool: True if seminars have been scheduled, False if not
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
            course_time_table[day][time_slot] = room, group
            room_time_table[day][time_slot] = course, group

            # Update time table of the students
            for student in group:
                student_time_table = student.get_time_table()
                student_time_table[day][time_slot].append((room, course, "Sem"))

    return True


def schedule_practicum(course: Course, available_rooms: list[Room]) -> bool:
    """
    Schedules all practicals needed to be given for the given Course. These
    are all randomly scheduled.

    Args:
        course (Course): Course to be scheduled
        available_rooms (list[Room]): The available room time slots

    Returns:
        bool: True if practicals have been scheduled, False if not
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
            course_time_table[day][time_slot] = room, group
            room_time_table[day][time_slot] = course, group

            # Update time tables of the students
            for student in group:
                student_time_table = student.get_time_table()
                student_time_table[day][time_slot].append((room, course, "Prac"))

    return True
