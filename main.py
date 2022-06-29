#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Created By  :
# Created Date:
# ---------------------------------------------------------------------------
from __future__ import annotations

from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room

from src.schedule_validity.schedule_validity import is_valid_schedule
from src.loader.loader import load_students, load_rooms, load_courses
from src.algorithm.random_scheduling import schedule_course
from src.algorithm.Completely_random import random_schedule_course
from src.algorithm.restart_hillclimb import hill_climb_restart
from src.algorithm.sim_annealing import start_annealing

# from src.algorithm.greedy import greedy
from src.malus_point_count import malus_point_count, conflict_count
from src.algorithm.hillclimber import hill_climb
from src.algorithm.greedy import greedy_schedule_course


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from csv import DictWriter
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


def main():
    # run_algorithm(True)

    n_hill_climbs = 1000
    data = []
    end_values = []
    best_points = float("inf")
    best_time_table = []

    computation_times = []

    for i in range(n_hill_climbs):
        begin = time()
        if i != 0:
            average_time = sum(computation_times) / len(computation_times)
            print(
                f"Estimated time left: {ceil((average_time*(n_hill_climbs-i))/60)} minutes"
            )
        print(f"Simulation {i} out of {n_hill_climbs}")

        points, time_table = run_algorithm()

        end_value = points[-1]

        end_values.append(end_value)
        data += points

        if end_value < best_points:
            best_points = end_value
            best_time_table = deepcopy(time_table)

        end = time()
        duration = end - begin
        computation_times.append(duration)

    print(f"best timetable found: {min(data)} malus points")

    # df = pd.DataFrame(best_time_table)
    # df.columns = ["Student", "Course"]

    # df.to_csv("output/output_time_table.csv")

    mu = np.mean(end_values)
    sigma = np.std(end_values)

    normal_dist = np.random.normal(mu, sigma, 1000)

    count, bins, ignored = plt.hist(normal_dist, 30, density=True)
    plt.plot(
        bins,
        1
        / (sigma * np.sqrt(2 * np.pi))
        * np.exp(-((bins - mu) ** 2) / (2 * sigma**2)),
        linewidth=2,
        color="r",
    )

    # plt.xlabel("Malus Points")
    # plt.grid(which="both")
    # plt.savefig("docs/hillclimb_normal_dist_fifth_hour.png")

    # plt.bar(data)

    # plt.ylabel("N")
    # plt.xlabel("Malus Points")

    # plt.grid(which="both")

    # plt.savefig("docs/random_barplot.png")

    # plt.plot(data)

    # plt.ylabel("Malus Points")
    # plt.xlabel("Iterations")

    # plt.grid(which="both")

    # plt.savefig("docs/sim_anneal.png")


def run_algorithm(verbose=True):

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

    # -----------------------Create a timetable-------------------------------------------
    available_rooms = []

    # Create a list of all available rooms, with all available time slots
    for room in rooms.values():
        for day in range(len(DAYS)):
            for time_slot in range(4):
                available_rooms.append((room, day, time_slot))

    # Schedule all courses
    for course in courses_sorted:
        schedule_course(course, available_rooms)

    # added schedule validity
    if not is_valid_schedule(students, rooms):
        print("not a valid schedule")
        return

    malus_points = malus_point_count(students, rooms)

    room_count_table = [[7] * 4 for _ in range(5)]

    if verbose:
        print_2d_list(students[16])

    available_rooms += [(rooms["C0.110"], day, 4) for day in range(5)]

    malus_points_progress = hill_climb_restart(
        courses_sorted, available_rooms, students, rooms
    )

    malus_points_progress = []

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
    main()
