from __future__ import annotations

from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room

from src.malus_point_count import malus_point_count
from src.reschedule.reschedule import reschedule_time_slot

import random


def start_annealing(
    courses: list[Course],
    room_time_slots: list,
    students: list[Student],
    rooms: list[Room],
    starting_temp: float,
) -> list[int]:
    """
    This function calls the simulated_annealing() function. This function keeps on
    calling the the simulated_annealing() function untill there is no improvement
    in the state for 2000 iterations. After this the function returns all points
    from beginning till end of the simulated annealing.

    Args:
        courses (list[Course]): list of all course objects
        room_time_slots (list): list of all room timeslots
        students (list[Student]): list of all student objects 
        rooms (list[Room]): list of all room objects 
        starting_temp (int): temperature to start the simulated annealing with

    Returns:
        int: amount of malus points
    """

    malus_points = []
    same_value_count = 0
    old_points = float("inf")

    iterations = 10000

    for i in range(iterations):
        new_points = simulated_annealing(
            courses, room_time_slots, students, rooms, starting_temp, i, iterations)

        if old_points == new_points:
            same_value_count += 1
        else:
            same_value_count = 0

        old_points = new_points
        malus_points.append(new_points)

    return malus_points


def simulated_annealing(
    courses: list[Course],
    room_time_slots: list,
    students: list[Student],
    rooms: list[Room],
    starting_temp: float,
    current_iteration: int,
    iterations
) -> int:
    """
    simulated_annealing() works very similair to the restart hillclimber, however it has
    a slight difference.
    The function works by making a change to the state of the time_table and comparing
    the points before and after the change. If the points are lower (better), the new state is
    accepted. If the new points are higher (worse) the state has a chance to be accepted.
    This chance lowers exponentionally, the worse the new points are.
    The accepting chance is also dependent on how many iterations in the anealling is.
    Meaning the longer this algorithm goes on, the less the chance becomes on accepting a
    worse change.

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
    if new_points > old_points:
        temp = starting_temp - (starting_temp/iterations) * current_iteration
        accept_chance = 2 ** ((old_points - new_points) / temp)

        if random.random() > accept_chance:
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
