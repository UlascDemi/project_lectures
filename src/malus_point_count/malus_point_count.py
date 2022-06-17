from __future__ import annotations

from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room

def conflict_count(students: list[Student]) -> int:
    """_summary_

    Args:
        students (list[Student]): _description_

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


# def oud_tussenuur_count(students: list[Student]) -> int:
#     tussen_uur_maluspunt = 0
#     for student in students:
#         for day in student.get_time_table():
#             for i, _ in enumerate(day[:-2]):
#                 if len(day[i]) != 0 and len(day[i + 1]) == 0 and len(day[i + 2]) != 0:
#                     tussen_uur_maluspunt += 1
#             for i, _ in enumerate(day[:-3]):
#                 if len(day[i]) != 0 and len(day[i + 1]) == 0 and len(day[i + 2]) == 0 and  len(day[i + 3]) != 0:
#                     tussen_uur_maluspunt += 3
#     # als we een 5de tijdslot hebben moet er een try and except in komen anders index out of bounce
#     return tussen_uur_maluspunt


def free_period_count(students: list[Student]) -> int:
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
                elif free_periods > 2:
                    print("ERROR: more than two free periods")

    return free_period_points


def fifth_hour_points(rooms: dict[Room]) -> int:
    malus_points = 0

    room = rooms["C0.110"]
    time_table = room.get_time_table()

    for day in time_table:
        if day[4] != "-":
            malus_points += 5

    return malus_points


def capacity_count(rooms: dict[Room]) -> int:
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
    conflicts = conflict_count(students)
    free_periods = free_period_count(students)
    capacity_conflict = capacity_count(rooms)
    fifth_hour = fifth_hour_points(rooms)

    maluspoint = conflicts + free_periods + capacity_conflict + fifth_hour

    return maluspoint