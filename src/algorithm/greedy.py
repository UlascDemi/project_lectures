from __future__ import annotations

from matplotlib.pyplot import get
from src.algorithm.hillclimber import reschedule_time_slot
from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room
from src.algorithm.Completely_random import random_schedule_course
import numpy as np

import random

from src.malus_point_count.malus_point_count import malus_point_count

# Kiest geen random optie: telkens de beste
# Loop door courses: plant de course in en berekent voor alle mogelijkheden
# de maluspunten. Wanneer de maluspunten het laagst zijn plant hij hem def in

# Letten op: random bv op basis van veel maluspunten uit random.
# available_rooms:
# Slide maken waarom je greedy op welk probleem: werkte wel of niet
# Stap 1. vind tijdslot
# Stap 2. welke kamers zijn beschikbaar (availablerooms)
# Stap 3. kies eentje waarvan de minste capaciteit nodig is?


def get_choosable_rooms(
    room_time_slots: list[tuple[Room, int, int]], min_capacity: int, day, time_slot
) -> list:
    """
    Returns a list containing all room time slots that are available and have enough
    capacity.
    This function expects a list with room time slots and an integer representing the
    minimum capacity amount. The room time slot is in the format of a tuple containing
    three elements: (Room, day, time_slot). Where Room is a Room object and the day and
    time_slot are represented by an int. In this case (Room1, 0, 0) would be room 1 on
    monday with the first time slot.
    the function returns a list in the same format as the input list with the room time
    slots that have enough capacity

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
        and room_time_slot[1] == day
        and room_time_slot[2] == time_slot
    ]

    return choosable_rooms


def get_best_room_time_slot(room_count_table: list[list]) -> bool:
    """
    Returns coordinates of timeslot with the most available rooms at that moment. 
    If there are multiple timeslots with the most available rooms the function will choose
    one of these randomly. When the coordinates are given the available room count will be
    updated.

    Args:
        room_count_table (list): 2d array of all time slots and available room count

    Returns:
       int : x and y coordinate 
    """
    max_value = np.max(room_count_table)
    max_value_indices = np.argwhere(room_count_table == max_value)

    max_value_index = random.choice(max_value_indices)
    best_i = max_value_index[0]
    best_j = max_value_index[1]
    room_count_table[best_i][best_j] -= 1
    return best_i, best_j


def greedy_schedule_course(course: Course, available_rooms: list[Room], room_count_table:
    list[list]) -> bool:
    """
    Returns true if every lecture, seminar and practical is scheduled.
    This functions schedules every lecture, seminar and practical in a greedy manner. It schedules every course
    based on the room availabilty of a timeslot. It prioritizes timeslots with higher 
    room availability.

    Args:
        course (Course): course objects
        available_rooms (list[Room]): list of available rooms
        room_count_table (list[list]): 2d array of timeslots

    Returns:
        bool : Returns True if every course aspect is scheduled
    """
    if (
        schedule_lecture(course, available_rooms, room_count_table)
        and schedule_seminar(course, available_rooms, room_count_table)
        and schedule_practicum(course, available_rooms, room_count_table)
    ):
        return True


def schedule_lecture(course: Course, available_rooms: list[Room], room_count_table:
    list[list]) -> bool:
    """
    Returns true if every lecture of a course is scheduled.
    This functions schedules every lecture in a greedy manner. It schedules every course
    based on the room availabilty of a timeslot. It prioritizes timeslots with higher 
    room availability.

    Args:
        course (Course): course objects
        available_rooms (list[Room]): list of available rooms
        room_count_table (list[list]): 2d array of timeslots

    Returns:
        bool: returns true if every lecture is scheduled
    """
    for _ in range(course.n_lecture):
        # Checks if lectures need to be given
        if course.n_lecture == 0:
            return True

        minimum_cap = course.get_n_enrol_students()
        best_day, best_time_slot = get_best_room_time_slot(room_count_table)
        choosable_rooms = get_choosable_rooms(
            available_rooms, minimum_cap, best_day, best_time_slot
        )

        # Remove time slot from available room time slots list
        if len(choosable_rooms) != 0:
            for available_room in set(choosable_rooms):
                if (
                    available_room[1] == best_day
                    and available_room[2] == best_time_slot
                ):

                    room, day, time_slot = available_room
                    available_rooms.remove(available_room)
                    break
        else:
            for available_room in set(available_rooms):
                if (
                    available_room[1] == best_day
                    and available_room[2] == best_time_slot
                ):

                    room, day, time_slot = available_room
                    available_rooms.remove(available_room)
                    break

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


def schedule_seminar(
    course: Course, available_rooms: list[Room], room_count_table: list[list]
) -> bool:
    """
    Returns true if every seminar group  of a course is scheduled.
    This functions schedules every seminar group in a greedy manner. It schedules every course
    based on the room availabilty of a timeslot. It prioritizes timeslots with higher 
    room availability.

    Args:
        course (Course): course objects
        available_rooms (list[Room]): list of available rooms
        room_count_table (list[list]): 2d array of timeslots

    Returns:
        bool: returns true if every lecture is scheduled
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

            best_day, best_time_slot = get_best_room_time_slot(room_count_table)
            choosable_rooms = get_choosable_rooms(
                available_rooms, minimum_cap, best_day, best_time_slot
            )

            if len(choosable_rooms) != 0:
                for available_room in set(choosable_rooms):
                    if (
                        available_room[1] == best_day
                        and available_room[2] == best_time_slot
                    ):

                        room, day, time_slot = available_room
                        available_rooms.remove(available_room)
                        break
            else:
                for available_room in set(available_rooms):
                    if (
                        available_room[1] == best_day
                        and available_room[2] == best_time_slot
                    ):

                        room, day, time_slot = available_room
                        available_rooms.remove(available_room)
                        break

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


def schedule_practicum(
    course: Course, available_rooms: list[Room], room_count_table: list[list]
) -> bool:
    """
    Returns true if every seminar group  of a course is scheduled.
    This functions schedules every seminar group in a greedy manner. It schedules every course
    based on the room availabilty of a timeslot. It prioritizes timeslots with higher 
    room availability.

    Args:
        course (Course): course objects
        available_rooms (list[Room]): list of available rooms
        room_count_table (list[list]): 2d array of timeslots

    Returns:
        bool: returns true if every lecture is scheduled
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
            # Remove time slot from available room time slots list
            best_day, best_time_slot = get_best_room_time_slot(room_count_table)
            choosable_rooms = get_choosable_rooms(
                available_rooms, minimum_cap, best_day, best_time_slot
            )

            if len(choosable_rooms) != 0:
                for available_room in set(choosable_rooms):
                    if (
                        available_room[1] == best_day
                        and available_room[2] == best_time_slot
                    ):

                        room, day, time_slot = available_room
                        available_rooms.remove(available_room)
                        break
            else:
                for available_room in set(available_rooms):
                    if (
                        available_room[1] == best_day
                        and available_room[2] == best_time_slot
                    ):

                        room, day, time_slot = available_room
                        available_rooms.remove(available_room)
                        break

            # print(room_count_table)
            # print(choosable_rooms)
            # print(available_rooms)
            # print(best_day, best_time_slot)
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
