from __future__ import annotations

from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room

from src.malus_point_count import malus_point_count
from src.reschedule.reschedule import reschedule_time_slot
from src.schedule_validity.schedule_validity import third_free_period_check

import random


def hill_climb(
    courses: list[Course],
    room_time_slots: list,
    students: list[Student],
    rooms: list[Room],
) -> int:
    """
    The hill_climb algorithm works by taking a random course, then a random time slot of
    the course. This time slot is then rescheduled to another time slot. The malus points
    are then calculated and compared to the malus points before the reschedule.
    If the points are worse than before, the course is reverted to its original state.
    The new time slot is taken from the room_time_slots. This is a list containing all
    available room time slots.

    Args:
        courses (list[Course]): a list of all courses
        room_time_slots (list): a list with all time_slots in the format of: (room, day, time_slot)
        students (list[Student]): a list with all students
        rooms (list[Room]): a list with all rooms

    Returns:
        int: the malus points of the resulting state
    """

    old_points = malus_point_count(students, rooms)

    course = random.choice(courses)
    time_table = course.get_time_table()
    
    filled_in_slots = get_filled_in_slots(time_table)

    # Choose the course that needs to be moved and choose a new time_slot
    original_day_time_slot = random.choice(filled_in_slots)
    new_time_slot = random.choice(room_time_slots)

    reschedule_time_slot(course, room_time_slots, original_day_time_slot, new_time_slot)

    new_points = malus_point_count(students, rooms)

    # Check if the new schedule is better, if worse, revert back
    if new_points > old_points or third_free_period_check(students):
        reschedule_time_slot(
            course, room_time_slots, new_time_slot, original_day_time_slot
        )

        return old_points

    return new_points


def get_filled_in_slots(time_table) -> list:
    """
    Checks for timeslots in timetable if its filled.

    Args:
        time_table (list[list]): 2d array 

    Returns:
        list: list of filled timeslots
    """
    filled_in_slots = []

    # Find all non-empty timeslots in time_table
    for i, _ in enumerate(time_table):
        for j, value in enumerate(time_table[i]):
            if time_table[i][j] != "-":
                filled_in_slots.append((value[0], i, j))

    return filled_in_slots
