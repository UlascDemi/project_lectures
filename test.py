from __future__ import annotations

from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room

# Dit zou 1 maluspunt moeten zijn
time_table_1 = [
    [[1],[1],[],[1],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]]
]


# Dit zou 3 maluspunten moeten zijn
time_table_2 = [
    [[],[],[],[],[]],
    [[],[1],[],[],[1]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]]
]

# Dit zou 5 maluspunten moeten zijn
time_table_3 = [
    [[],[],[],[],[]],
    [[],[],[],[],[1]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]]
]

# Dit zou 1 maluspunten moeten zijn
time_table_4 = [
    [[],[1,1],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]]
]

# schedule validity is false 
time_table_5 = [
    [[1],[],[],[],[1]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]]
]

# maluspunten 2 (2 conflicten)
time_table_6 = [
    [[1,1],[1,1],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]]
]

# maluspunten 3 (2 conflict & 1 tussenuur)
time_table_7 = [
    [[1,1],[],[1,1],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]]
]

# maluspunten = 8 (2 tussenuur & 5e)
time_table_8 = [
    [[],[],[],[],[]],
    [[],[1],[],[],[1]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]]
]

# maluspunten = 1 conflict 
time_table_9 = [
    [[],[],[],[],[]],
    [[1],[],[],[],[]],
    [[1,1],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]]
]

def tussenuur_count(students) -> int:
    tussen_uur_maluspunt = 0

    # for student in students:
    for day in students:
        activiteit = 0
        first_activity = None
        last_activity = None

        for i, time_slot in enumerate(day):
            if len(time_slot) != 0:
                if activiteit == 0:
                    first_activity = i
                activiteit += 1
                last_activity = i
        
        if first_activity != last_activity:    
            amount_activities = last_activity - first_activity +1
            tussen_uren = amount_activities - activiteit

            if tussen_uren == 1:
                tussen_uur_maluspunt += 1
            elif tussen_uren == 2:
                tussen_uur_maluspunt += 3
            elif tussen_uren > 2:
                print("ERROR: more than two free periods")

    return tussen_uur_maluspunt


def conflict_count(time_table) -> int:
    """
     Checks for every student if a timeslot has more than one course planned.
     for each extra course that is given a malus points will be added.

    Args:
        students (list[Student]): list of student objects

    Returns:
        int: total amount of conflicting timeslots
    """
    conflict_count = 0

    # Go through every time day and timeslot
    for day in time_table:
        for time_slot in day:

            # If the timeslot has more than 1 entry, count the excess amount
            if len(time_slot) > 1:
                conflict_count += len(time_slot) - 1

    return conflict_count


def fifth_hour_points(time_table) -> int:
    """
    Checks if the 5th timeslot is used for the room C0.110.
    Room schedules get 5 malus points if this timeslot is used

    Args:
        rooms (dict[Room]): dictionairy with room objects

    Returns:
        int: total amount of malus points
    """
    malus_points = 0

    for day in time_table:
        if len(day[4]) != 0:
            malus_points += 5

    return malus_points



print(f"timetable 1 moet 1 maluspunt zijn en is: {tussenuur_count(time_table_1)}")
print(f"timetable 2 moet 3 maluspunten zijn en is: {tussenuur_count(time_table_2)}")
print(f"timetable 3 moet 5 maluspunten zijn en is: {fifth_hour_points(time_table_3)}")
print(f"timetable 4 moet 1 maluspunt zijn en is: {conflict_count(time_table_4)}")
print(f"timetable 5 kan niet ivm 3 tussenuur en is: {tussenuur_count(time_table_5)}")
print(f"timetable 6 moet 2 maluspunten zijn en is: {conflict_count(time_table_6)}")
maluspunt7 = tussenuur_count(time_table_7) + conflict_count(time_table_7)
print(f"timetable 7 moet 3 maluspunten zijn en is: {maluspunt7}")

maluspunt8 = tussenuur_count(time_table_8) + fifth_hour_points(time_table_8)
print(f"timetable 8 moet 8 maluspunten zijn en is: {maluspunt8}")

maluspunt9 = tussenuur_count(time_table_9) + conflict_count(time_table_9)
print(f"timetable 9 moet 1 maluspunt zijn en is: {maluspunt9}")


