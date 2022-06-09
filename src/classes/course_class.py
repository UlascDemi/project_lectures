import numpy as np
from math import ceil


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

        # # Calculate amount of classes needed for one seminar
        # self._class_per_seminar = ceil(self._expected_students / self._seminar_cap)

        # # Calculate total needed classes for all seminars
        # self._needed_seminars = self._n_seminar * self._class_per_seminar

        # # Calculate students per seminar
        # self._students_per_seminar = ceil(
        #     self._expected_students / self._class_per_seminar
        # )

        # # TODO hoeveelheid studenten per practicum berekenen, net als hierboven ^

    def get_expected_stud(self) -> None:
        return self._expected_students

    def set_expected_stud(self, value) -> None:
        self._expected_students = value
