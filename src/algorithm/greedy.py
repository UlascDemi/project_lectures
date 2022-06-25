from __future__ import annotations
from src.algorithm.hillclimber import reschedule_time_slot
from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room

import random

from src.malus_point_count.malus_point_count import malus_point_count

# Kiest geen random optie: telkens de beste
# Loop door courses: plant de course in en berekent voor alle mogelijkheden
# de maluspunten. Wanneer de maluspunten het laagst zijn plant hij hem def in

def greedy(course: Course, available_rooms: list[Room], students: list[Student], rooms: dict[Room]):
    
    # Loop door de courses:
    for course in courses_sorted:
        
        # plan course in
        schedule_course(course, available_rooms)

        maluspunten = malus_point_count(students, rooms)
        if maluspunten == 0:
             schedule_course(course, available_rooms)
        else:
            for timeslot in available_rooms:
                reschedule_time_slot
