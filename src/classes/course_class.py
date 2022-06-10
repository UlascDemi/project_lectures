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
        self._enrolled_students = []

        self._class_per_seminar = 0
        self._needed_seminars = 0
        self._students_per_seminar = 0

        self._class_per_practicum = 0
        self._needed_practica = 0
        self._students_per_practicum = 0

        # TODO misschien dit weg, want we krijgen de hoeveelheid studenten al via enroll()
        self.calc_seminars()
        self.calc_practica()

    def enroll(self, student) -> None:
        self._enrolled_students.append(student)

    def calc_practica(self) -> None:
        """_summary_"""
        if self._n_practica != 0:

            # Calculate amount of classes needed for one practicum
            self._class_per_practicum = ceil(self._expected_students / self._pract_cap)

            # Calculate total needed classes for all practicum
            self._needed_practica = self._n_practica * self._class_per_practicum

            # Calculate students per seminar
            self._students_per_practicum = ceil(
                self._expected_students / self._class_per_practicum
            )

    def calc_seminars(self) -> None:
        """_summary_"""
        if self._n_seminar != 0:

            # Calculate amount of classes needed for one seminar
            self._class_per_seminar = ceil(self._expected_students / self._seminar_cap)

            # Calculate total needed classes for all seminars
            self._needed_seminars = self._n_seminar * self._class_per_seminar

            # Calculate students per seminar
            self._students_per_seminar = ceil(
                self._expected_students / self._class_per_seminar
            )

    def get_course_name(self) -> str:
        """
        Returns the name of the course

        Returns:
            str: the name of the course
        """
        return self._course_name

    def get_n_lecture(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        return self._n_lecture

    def get_expected_stud(self) -> None:
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._expected_students

    def set_expected_stud(self, value) -> None:
        """_summary_

        Args:
            value (_type_): _description_
        """
        self._expected_students = value
