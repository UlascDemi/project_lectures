from __future__ import annotations
from src.algorithm.hillclimber import reschedule_time_slot
from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room

import random

from src.malus_point_count.malus_point_count import malus_point_count


def greedy(course: Course, available_rooms: list[Room], students: list[Student], rooms: dict[Room]):
    for course in courses_sorted:
        maluspunten = malus_point_count(students, rooms)
        if maluspunten == 0:
             schedule_course(course, available_rooms)
        else:
            for timeslot in available_rooms:
                reschedule_time_slot