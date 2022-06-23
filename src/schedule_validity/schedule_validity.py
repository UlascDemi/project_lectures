from __future__ import annotations
from copy import deepcopy
from src.classes.student import Student
from src.classes.room import Room

schedule_validity = True


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
                    print("ERROR: more than two free periods")
                    return False 


def room_conflict_check(rooms: dict[Room]) -> int:
    """
    Checks if a room has more than one activity planned in one timeslot

    Args:
        rooms (dict[Room]): contains room objects

    """

    # Go through every room
    for room in rooms.values():
        time_table = room.get_time_table()

        # Go through every time day and timeslot
        for day in time_table:
            for time_slot in day:

                # If the timeslot has more than 1 entry, count the excess amount
                if len(time_slot) > 1:
                    print("ERROR: more than two activities planned in one room")
                    return False
    
def fifth_hour_check(rooms: dict[Room]) -> int:
    """
    Checks if a room has more than one activity planned in one timeslot

    Args:
        rooms (dict[Room]): contains room objects

    """

    # Go through every room
    copy = deepcopy(rooms)
    del copy["C0.110"]
    for room in copy.values():
        time_table = room.get_time_table()

        # Go through every time day and timeslot
        for day in time_table:
            for time_slot in day:

                # If the timeslot has more than 1 entry, count the excess amount
                if day[4] != "-":
                    print("ERROR: fifth hour timeslot is use in other rooms than C0.110")
                    
                    return False
def schedule_validity(students, rooms):
    validity = True
    if fifth_hour_check(rooms) or third_free_period_check or room_conflict_check is False:
        validity = False
    return validity