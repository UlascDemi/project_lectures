from __future__ import annotations
from copy import deepcopy
from src.classes.student import Student
from src.classes.room import Room


def third_free_period_check(students: list[Student]) -> int:
    """
    Check if a student has a third free period.

    Args:
        students (list[Student]): list of student object

    """

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

                if free_periods > 2:
                    return False

    return True


def fifth_hour_check(rooms: dict[Room]) -> bool:
    """
    Checks if the fifth time slot of other rooms except C0.110 is used.

    Args:
        rooms (dict[Room]): dictionairy of every room object

    Returns:
        bool: returns true fifth hour is used
    """

    for room in rooms.values():
        if room == rooms["C0.110"]:
            continue

        for day in room.get_time_table():
            if day[4] != "-":
                return False

    return True


def is_valid_schedule(students: list[Student], rooms: dict[Room]):
    """
    Checks if valid schedules are created based on fifth hour check and third free 
    period check. Returns true the schedules passed the checks. 

    Args:
        students (list[Student]): list of all student objects
        rooms (dict[Student]): dictionairy of all room objects

    Returns:
        bool: returns true if fifth hour checks and third free period check are passed
    """

    if fifth_hour_check(rooms) and third_free_period_check(students):
        return True

    return False
