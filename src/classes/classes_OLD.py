#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Created By  :
# Created Date: 31-05-2022
# ---------------------------------------------------------------------------
"""
"""
import numpy as np
from math import ceil


class Student:
    def __init__(
        self, first_name: str, last_name: str, student_num: str, courses: list
    ) -> None:

        self._first_name = first_name
        self._last_name = last_name
        self._studentnumber = student_num
        self._courses = courses
        self._timetable = np.array([5, 5])  # hierin komt een tuple: (Room, Course)


class Room:
    def __init__(self, roomnumber, capacity):
        self._roomnumber = roomnumber
        self._capacity = capacity

        # hierin komt een tuple: (lijst[student_num], Course)
        self._timetable = np.array([5, 5])


class Course:
    def __init__(
        self,
        course,
        lecture,
        seminar,
        max_students_werk,
        practica,
        max_students_prac,
        expected,
    ):
        self._course_name = course
        self._n_lecture = lecture
        self._n_seminar = seminar
        self._n_practica = practica
        self._seminar_cap = max_students_werk
        self._pract_cap = max_students_prac
        self._expected_students = expected

        # Calculate amount of classes needed for one seminar
        self._class_per_seminar = ceil(self._expected_students / self._seminar_cap)

        # Calculate total needed classes for all seminars
        self._needed_seminars = self._n_seminar * self._class_per_seminar

        # Calculate students per seminar
        self._students_per_seminar = ceil(
            self._expected_students / self._class_per_seminar
        )

        # TODO hoeveelheid studenten per practicum berekenen, net als hierboven ^

    def get_expected_stud(self) -> None:
        return self._expected_students

    def set_expected_stud(self, value) -> None:
        self._expected_students = value
