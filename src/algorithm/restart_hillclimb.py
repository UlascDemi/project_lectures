from __future__ import annotations

from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room

from src.algorithm.hillclimber import hill_climb


def hill_climb_restart(courses: list[Course], room_time_slots: list, students: list[Student], rooms: list[Room]):

    malus_points = []
    same_value_count = 0
    old_points = float('inf')

    # Continue hillclimbing untill no improvement is found in N steps
    while same_value_count < 2000:
        new_points = hill_climb(courses, room_time_slots, students, rooms)

        if old_points == new_points:
            same_value_count += 1
        else:
            same_value_count = 0

        old_points = new_points
        malus_points.append(new_points)

    return malus_points
