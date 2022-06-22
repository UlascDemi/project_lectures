from __future__ import annotations

from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room

from .random_scheduling import schedule_course
from src.malus_point_count import malus_point_count

import random

# DIT GAAT ERVANUIT DAT AL EEN GELDIGE ROOSTER IS GEMAAKT


def hill_climb(courses: list[Course], room_time_slots: list, students, rooms):
    # Take random
    old_points = malus_point_count(students, rooms)

    # course = random.choice(courses)
    course = courses[11]
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

    if not schedule_course(course, room_time_slots):
        schedule_course(course, [original_day_time_slot])
        print("aa")
        return course

    new_points = malus_point_count(students, rooms)

    if new_points <= old_points:
        # print(new_points)
        pass
    else:
        print("revert")
        schedule_course(course, [original_day_time_slot])

    print(malus_point_count(students, rooms))
    # print("")

    return course


def un_schedule(course: Course, available_rooms: list):
    time_table = course.get_time_table()

    students = course.get_enrol_students()

    for i, day in enumerate(time_table):
        for j, time_slot in enumerate(day):
            if time_slot != "-":
                for student in students:
                    student_time_slots = student.get_time_table()[i][j]
                    for k, (room_object, course_object, type) in enumerate(
                        student_time_slots
                    ):
                        if room_object == time_slot and course_object == course:
                            student_time_slots.pop(k)
                time_slot.get_time_table()[i][j] = "-"

                available_rooms.append((time_slot, i, j))
                time_table[i][j] = "-"

    def reschedule_course(course: Course, available_rooms: list, new_time_slot) -> None:
        pass
        # 1
