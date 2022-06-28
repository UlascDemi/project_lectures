from __future__ import annotations

from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room

from src.algorithm.hillclimber import hill_climb


def hill_climb_restart(
    courses: list[Course],
    room_time_slots: list,
    students: list[Student],
    rooms: list[Room],
) -> list[int]:
    """
    The restart hill climber works by starting a hill climb, when no improvement is found for N amount of
    iterations, this functions returns a list of all malus points found during the hillclimbng for this
    starting position. The restart can be put in a for-loop to repeat the restarting.
    This algorithm assumes a random time table is already created and saved internally in the course,
    room and student objects.

    Args:
        courses (list[Course]): a list of all courses
        room_time_slots (list): a list of all available room time slots.
        students (list[Student]): a list of all students
        rooms (list[Room]): a list of all rooms

    Returns:
        list[int]: a list containing the malus points
    """
    malus_points = []
    same_value_count = 0
    old_points = float("inf")

    threshold = 2000

    # Continue hillclimbing untill no improvement is found in N steps
    while same_value_count < threshold:
        new_points = hill_climb(courses, room_time_slots, students, rooms)

        if old_points == new_points:
            same_value_count += 1
        else:
            same_value_count = 0

        old_points = new_points
        malus_points.append(new_points)

    return malus_points
