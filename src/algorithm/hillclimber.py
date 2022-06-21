from __future__ import annotations

from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room

from .random_scheduling import schedule_course
from src.malus_point_count import malus_point_count

import random

# DIT GAAT ERVANUIT DAT AL EEN GELDIGE ROOSTER IS GEMAAKT


def hill_climb(courses: list[Course], room_time_slots: list,  students, rooms):
    # Take random
    old_points = malus_point_count(students, rooms)

    course = random.choice(courses)
    day = random.choice(course.get_time_table())
    time_slot = random.choice(day)

    iteration = 0
    new_day_chosen = 0

    while time_slot == "-":
        if iteration > 30:
            iteration = 0
            new_day_chosen += 1

            day = random.choice(course.get_time_table())
            if new_day_chosen > 10:
                course = random.choice(courses)
                new_day_chosen = 0

        time_slot = random.choice(day)

        iteration += 1

    original_day_time_slot = (day, time_slot)

    if not schedule_course(course, room_time_slots):
        return False

    new_points = malus_point_count(students, rooms)

    if new_points >= old_points:
        print(new_points)
    else:
        schedule_course

    # put somewhere else

    # compare points

    # exit()
