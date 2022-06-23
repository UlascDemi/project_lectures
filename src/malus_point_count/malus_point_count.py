from __future__ import annotations

from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room

def conflict_count(students: list[Student]) -> int:
    """
     Checks for every student if a timeslot has more than one course planned.
     for each extra course that is given a malus points will be added.

    Args:
        students (list[Student]): list of student objects 

    Returns:
        int: total amount of conflicting timeslots
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


def free_period_count(students: list[Student]) -> int:
    """ 
    Checks if for every student if their schedule has free period between classes.
    Students schedules with 1 free periods between classes get 1 malus point.
    Students schedules with 2 free periods between classes get 3 malus points.

    Args:
        students (list[Student]): list of student objects

    Returns:
        int: total amount of malus points
    """
    free_period_points = 0

    for student in students:
        for day in student.get_time_table():
            activity = 0
            first_activity = None
            last_activity = None

            for i, time_slot in enumerate(day):
                if len(time_slot) != 0:
                    if activity == 0:
                        first_activity = i
                    activity += 1
                    last_activity = i

            if first_activity != last_activity:
                amount_activities = last_activity - first_activity + 1
                free_periods = amount_activities - activity

                if free_periods == 1:
                    free_period_points += 1
                elif free_periods == 2:
                    free_period_points += 3

    return free_period_points


def fifth_hour_points(rooms: dict[Room]) -> int:
    """
    Checks if the 5th timeslot is used for the room C0.110.
    Room schedules get 5 malus points if this timeslot is used

    Args:
        rooms (dict[Room]): dictionairy with room objects

    Returns:
        int: total amount of malus points 
    """
    malus_points = 0

    room = rooms["C0.110"]
    time_table = room.get_time_table()

    for day in time_table:
        if day[4] != "-":
            malus_points += 5

    return malus_points


def capacity_count(rooms: dict[Room]) -> int:
    """
    Checks for class that is scheduled if the room capacity is exceeded.
    For every extra student that exceeds the room capacity a malus point is added.

    Args:
        rooms (dict[Room]): dictionairy of room names and room objects

    Returns:
        int: total amount of malus points
    """
    excess_students = 0

    for room in rooms.values():
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


def malus_point_count(students: list[Student], rooms: dict[Room]):
    """
    Add all malus points function together 

    Args:
        students (list[Student]): list of student objects
        rooms (dict[Room]): dictionairy of room names and room objects

    Returns:
        int: total amount of malus point
    """
    conflicts = conflict_count(students)
    print(f"conflicts: {conflicts}")
    free_periods = free_period_count(students)
    print(f"free periods: {free_periods}")
    capacity_conflict = capacity_count(rooms)
    print(f"capacity count: {capacity_conflict}")
    fifth_hour = fifth_hour_points(rooms)
    print(f"fifth hour: {fifth_hour}")

    maluspoint = conflicts + free_periods + capacity_conflict + fifth_hour

    return maluspoint