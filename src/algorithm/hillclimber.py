from __future__ import annotations

from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room

from .random_scheduling import schedule_course
from src.malus_point_count import malus_point_count

import random
from copy import copy, deepcopy

# DIT GAAT ERVANUIT DAT AL EEN GELDIGE ROOSTER IS GEMAAKT


def hill_climb(courses: list[Course], room_time_slots: list, students, rooms):

    old_points = malus_point_count(students, rooms)

    course = random.choice(courses)

    time_table = course.get_time_table()

    filled_in_slots = []

    for i, _ in enumerate(time_table):
        for j, value in enumerate(time_table[i]):
            if time_table[i][j] != "-":
                filled_in_slots.append((value[0], i, j))

    original_day_time_slot = random.choice(filled_in_slots)

    new_time_slot = random.choice(room_time_slots)

    reschedule_time_slot(course, room_time_slots, original_day_time_slot, new_time_slot)

    new_points = malus_point_count(students, rooms)

    if new_points > old_points:
        reschedule_time_slot(
            course, room_time_slots, new_time_slot, original_day_time_slot
        )


def reschedule_time_slot(
    course: Course, room_time_slots: list, start_time_slot, end_time_slot
) -> None:

    if len(room_time_slots) != 11:
        print("aaaaaa")
        breakpoint()

    # Unpack the time_slot tuples
    start_room, start_day_i, start_time_slot_i = start_time_slot
    end_room, end_day_i, end_time_slot_i = end_time_slot

    course_time_table = course.get_time_table()

    # Take the contents of the course time slot
    room, students = course_time_table[start_day_i][start_time_slot_i]

    # Remove the old time slot and put contents in new time slot
    course_time_table[start_day_i][start_time_slot_i] = "-"
    course_time_table[end_day_i][end_time_slot_i] = end_room, students

    start_room_time_table = start_room.get_time_table()
    end_room_time_table = end_room.get_time_table()

    # Remove old time slot from the room timetable and put contents in new time slot
    if end_room.get_time_table()[end_day_i][end_time_slot_i] != "-":
        print("we fucked up")
        print(end_day_i, end_time_slot_i)
        breakpoint()

    start_room_time_table[start_day_i][start_time_slot_i] = "-"
    end_room_time_table[end_day_i][end_time_slot_i] = course, students

    # Go through each student, remove the old time slot and put contents in new time slot
    for student in students:
        student_time_table = student.get_time_table()
        student_start_time_slot = student_time_table[start_day_i][start_time_slot_i]

        # Find correct activity and remove it from the time slot
        for activity in student_start_time_slot:
            scheduled_room = activity[0]
            type = activity[2]

            if scheduled_room == room:
                student_start_time_slot.remove(activity)

        # Append the activty to the new time_slot
        student_new_time_slot = student_time_table[end_day_i][end_time_slot_i]
        student_new_time_slot.append((end_room, course, type))

    room_time_slots.append(start_time_slot)
    room_time_slots.remove(end_time_slot)
