#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Created By  :
# Created Date:
# ---------------------------------------------------------------------------
from __future__ import annotations
import argparse

from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room

from src.schedule_validity.schedule_validity import is_valid_schedule
from src.loader.loader import load_students, load_rooms, load_courses
from src.algorithm.random_scheduling import schedule_course
from src.algorithm.Completely_random import random_schedule_course
from src.algorithm.restart_hillclimb import hill_climb_restart
from src.algorithm.sim_annealing import start_annealing

from src.malus_point_count import malus_point_count
from src.algorithm.greedy import greedy_schedule_course


import numpy as np
import pandas as pd

from tabulate import tabulate
from copy import deepcopy
from time import time
from math import ceil

# TODO getters voor course schrijven - Brechje
# TODO getters voor room schrijven - Ulas
# TODO getters voor student schrijven - Justin

# TODO docstrings in loader_pandas schrijven

# TODO een check maken of rooms niet overlappen

# TODO README

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIME_SLOTS = ["9:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", "17:00-19:00"]


def main(output: str, alg_type: str, n_simulations: int):
    assert alg_type in ["R", "G", "H", "A"]

    if alg_type == "R":
        alg_type = "random_schedule"
    elif alg_type == "G":
        alg_type = "greedy_algorithm"
    elif alg_type == "H":
        alg_type = "hill_climber"
    elif alg_type == "A":
        alg_type = "simulated_annealing"

    data = []
    end_values = []
    best_points = float("inf")
    best_time_table = []

    computation_times = []

    for i in range(n_simulations):
        begin = time()
        if i != 0:
            average_time = sum(computation_times) / len(computation_times)
            print(
                f"Estimated time left: {ceil((average_time*(n_simulations-i))/60)} minutes"
            )
        print(f"Simulation {i} out of {n_simulations}")

        points, time_table = run_algorithm(alg_type)

        end_value = points[-1]

        end_values.append(end_value)
        data += points

        if end_value < best_points:
            best_points = end_value
            best_time_table = deepcopy(time_table)

        end = time()
        duration = end - begin
        computation_times.append(duration)

    print(f"best timetable found: {best_points} malus points")

    df = pd.DataFrame(data)
    df.to_csv(output)

    # df = pd.DataFrame(best_time_table)
    # df.columns = ["Student", "Course"]

    # df.to_csv(output)


def run_algorithm(algr, verbose=False):

    rooms = load_rooms("data/zalen.csv")
    courses = load_courses("data/vakken.csv", "data/abbreviations.txt")
    students = load_students("data/studenten_en_vakken.csv")

    # -----------------------Enroll all students------------------------------------------
    for student in students:
        course_names = student.get_students_courses()
        for course_name in course_names:
            courses[course_name].enroll(student)

    courses_list = list(courses.values())
    courses_sorted = sorted(
        courses_list, key=lambda course: course.get_n_enrol_students(), reverse=True
    )
    # ----------------------Subdivide students into groups--------------------------------
    for course in courses_sorted:
        course.calc_seminars()
        course.calc_practica()

        course.subdivide_into_groups(
            course.get_groups_per_seminar(),
            course.get_stud_per_sem_group(),
            course.get_seminar_groups(),
        )

        course.subdivide_into_groups(
            course.get_groups_per_practicum(),
            course.get_stud_per_prac_group(),
            course.get_practicum_groups(),
        )

    # -----------------------Create the timetable-----------------------------------------
    available_rooms = []

    # Create a list of all available rooms, with all available time slots
    for room in rooms.values():
        for day in range(len(DAYS)):
            for time_slot in range(4):
                available_rooms.append((room, day, time_slot))

    if (
        algr == "random_schedule"
        or algr == "hill_climber"
        or algr == "simulated_annealing"
    ):
        # Schedule all courses
        for course in courses_sorted:
            schedule_course(course, available_rooms)

        if not is_valid_schedule(students, rooms):
            return

        if algr == "random_schedule":
            malus_points_progress = [malus_point_count(students, rooms)]

    malus_points = malus_point_count(students, rooms)

    if algr == "greedy_algorithm":
        room_count_table = [[7] * 4 for _ in range(5)]

        for course in courses_sorted:
            greedy_schedule_course(course, available_rooms, room_count_table)

        malus_points_progress = [malus_point_count(students, rooms)]

    if verbose:
        print_2d_list(students[16])

    if algr == "hill_climber" or algr == "simulated_annealing":
        available_rooms += [(rooms["C0.110"], day, 4) for day in range(5)]

        if algr == "hill_climber":
            malus_points_progress = hill_climb_restart(
                courses_sorted, available_rooms, students, rooms
            )
        elif algr == "simulated_annealing":
            malus_points_progress = start_annealing(
                courses_sorted, available_rooms, students, rooms, 9
            )

    if not is_valid_schedule(students, rooms):
        print("not a valid schedule")

    print(f"Start value = {malus_points}")
    print(f"End value = {malus_point_count(students, rooms)}")
    print("------------------------------------------------")

    student_time_tables = []

    # Create output a list for the output file
    for student in students:
        time_table = student.get_time_table()
        for day in time_table:
            for time_slot in day:
                student_time_tables.append([str(student), time_slot])

    return malus_points_progress, student_time_tables


def print_2d_list(object_to_print) -> None:

    # Make a copy of the time_table
    time_table = object_to_print.get_time_table()
    time_table_copy = deepcopy(time_table)

    if isinstance(object_to_print, Student):
        print(f"Timetable Student: {object_to_print}")

        # Reformat the copy to a printable format
        for i, _ in enumerate(time_table_copy):
            for j, time_slot in enumerate(time_table_copy[i]):
                if len(time_slot) == 0:
                    time_table_copy[i][j] = "-"
                else:
                    time_table_copy[i][j] = ", ".join(map(str, time_slot))

    elif isinstance(object_to_print, Course):
        print(f"Timetable Course: {object_to_print}")

        # Reformat the copy to a printable format
        for day in time_table_copy:
            for time_slot in day:
                time_slot = time_slot[0]
                print(time_slot)

    else:
        print(f"Timetable Room: {object_to_print}")

        # Reformat the copy to a printable format
        for day in time_table_copy:
            for time_slot in day:
                time_slot = time_slot[0]

    printable_list = np.transpose(np.array(time_table_copy, dtype=object))
    print(
        tabulate(printable_list, headers=DAYS, showindex=TIME_SLOTS, tablefmt="github")
    )


if __name__ == "__main__":

    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="Batch run a concert simulation")

    # Adding arguments
    parser.add_argument("output", help="output file (html)")
    parser.add_argument(
        "-a",
        "--algorithm_type",
        type=str,
        default="H",
        help="The type of algorithm. Choose from: [R / G / H / A] (default: H)",
    )
    parser.add_argument(
        "-s",
        "--n_simulations",
        type=int,
        default=1,
        help="The amount of simulations to be run (default: 1)",
    )

    args = parser.parse_args()

    main(args.output, args.algorithm_type, args.n_simulations)
