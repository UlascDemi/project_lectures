from __future__ import annotations

from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room

from .random_scheduling import schedule_course
from src.malus_point_count import malus_point_count

import random
from copy import copy

# DIT GAAT ERVANUIT DAT AL EEN GELDIGE ROOSTER IS GEMAAKT


def hill_climb(courses: list[Course], room_time_slots: list, students, rooms):
    # Take random
    old_points = malus_point_count(students, rooms)

    course = random.choice(courses)
    # course = courses[11]
    # print(course)

    time_table = course.get_time_table()
    day = random.choice(time_table)
    time_slot = random.choice(day)

    iteration = 0
    new_day_chosen = 0

    while time_slot == "-":
        if iteration > 30:
            iteration = 0
            new_day_chosen += 1

            day = random.choice(time_table)
            if new_day_chosen > 10:
                course = random.choice(courses)
                new_day_chosen = 0

        time_slot = random.choice(day)

        iteration += 1
        # day = random.choice(time_table)
        # time_slot = random.choice(day)

    original_day_time_slot = (
        time_slot,
        time_table.index(day),
        day.index(time_slot),
    )

    new_time_slot = random.choice(room_time_slots)

    reschedule_time_slot(course, room_time_slots, original_day_time_slot, new_time_slot)

    new_points = malus_point_count(students, rooms)

    if new_points > old_points:
        reschedule_time_slot(
            course, room_time_slots, new_time_slot, original_day_time_slot
        )


def reschedule_time_slot(
    course: Course, room_time_slots: list, orig_time_slot, new_time_slot
) -> None:

    # Unpack the time_slot tuples
    orig_room, orig_day_i, orig_time_slot_i = orig_time_slot
    new_room, new_day_i, new_time_slot_i = new_time_slot

    course_time_table = course.get_time_table()

    # Take the contents of the course time slot
    room, students = course_time_table[orig_day_i][orig_time_slot_i]

    # print(course_time_table[orig_day_i][orig_time_slot_i])

    # Remove the old time slot and put contents in new time slot
    course_time_table[orig_day_i][orig_time_slot_i] = "-"
    course_time_table[new_day_i][new_time_slot_i] = new_room, students

    room_time_table = room.get_time_table()

    # Remove old time slot from the room timetable and put contents in new time slot
    room_time_table[orig_day_i][orig_time_slot_i] = "-"
    room_time_table[new_day_i][new_time_slot_i] = course, students

    # Go through each student, remove the old time slot and put contents in new time slot
    for student in students:
        student_time_table = student.get_time_table()
        student_orig_time_slot = student_time_table[orig_day_i][orig_time_slot_i]

        # Find correct activity and remove it from the time slot
        for activity in student_orig_time_slot:
            scheduled_room = activity[0]
            type = activity[2]

            if scheduled_room == room:
                student_orig_time_slot.remove(activity)

        # Append the activty to the new time_slot
        student_new_time_slot = student_time_table[new_day_i][new_time_slot_i]
        student_new_time_slot.append((new_room, course, type))

    room_time_slots.append(orig_time_slot)
    room_time_slots.remove(new_time_slot)
