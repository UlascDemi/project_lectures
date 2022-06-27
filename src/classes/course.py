from __future__ import annotations

from src.classes import Student
from math import ceil


class Course:
    def __init__(
        self,
        course,
        abbreviation,
        lecture,
        seminar,
        max_students_werk,
        practica,
        max_students_prac,
        expected,
    ):
        self._course_name = course
        self._abbreviation = abbreviation

        self.n_lecture = lecture
        self.n_seminar = seminar
        self.n_practica = practica

        self._seminar_cap = max_students_werk
        self._pract_cap = max_students_prac

        self._expected_students = expected
        self._enrolled_students = []

        self._groups_per_seminar = 0
        self._students_per_sem_group = 0

        self._seminar_groups = []

        self._groups_per_practicum = 0
        self._students_per_prac_group = 0

        self._prac_groups = []
        # Creates 2D list representing the course time table
        self._time_table = [["-"] * 5 for i in range(5)]


    def enroll(self, student: Student) -> None:
        """
        Adds the enrolled students to the list 'enrolled_students'.

        Args:
            student (Student): Object of the student class
        """
        self._enrolled_students.append(student)


    def subdivide_into_groups(
        self, n_group: int, stud_per_group: int, groups: list
    ) -> None:
        """
        Function that goes through all students enrolled in a course and divides
        them into the subgroups.

        Args:
            n_group (int): Number of lessons to be given per class
            stud_per_group (int): Maximum number of students who can participate in a class
            groups (list): List where the groups need to subdived into
        """
        # If a lesson needs to be scheduled, walk through the enrolled students and
        # add the in the subgroup
        if n_group != 0:
            for i in range(0, self.get_n_enrol_students(), stud_per_group):
                groups.append(self.get_enrol_students()[i : i + stud_per_group])


    def calc_seminars(self) -> None:
        """
        When a course has seminars, it calculates how many groups should be given. This
        is determined based on the students enrolled in that course. This is because the
        seminars have a maximum number of students who can participate in the class.
        """
        if self.n_seminar != 0:

            # Calculate amount of groups needed for one seminar
            self._groups_per_seminar = ceil(
                self.get_n_enrol_students() / self._seminar_cap
            )

            # Calculate students per group
            self._students_per_sem_group = ceil(
                self.get_n_enrol_students() / self._groups_per_seminar
            )


    def calc_practica(self) -> None:
        """
        When a course has practica, it calculates how many groups should be given. This
        is determined based on the students enrolled in that course. This is because the
        practica have a maximum number of students who can participate in the class.
        """
        if self.n_practica != 0:

            # Calculate amount of classes needed for one practicum
            self._groups_per_practicum = ceil(
                self.get_n_enrol_students() / self._pract_cap
            )

            # Calculate total needed classes for all practicum
            self._needed_prac_groups = self.n_practica * self._groups_per_practicum

            # Calculate students per seminar
            self._students_per_prac_group = ceil(
                self.get_n_enrol_students() / self._groups_per_practicum
            )


    def get_course_name(self) -> str:
        """
        Returns the name of the course.

        Returns:
            str: the name of the course
        """
        return self._course_name


    def get_n_lecture(self) -> int:
        """
        Returns the amount of given lectures per week.

        Returns:
            int: amount of given lectures per week
        """
        return self.n_lecture


    def get_n_seminar(self) -> int:
        """
        Returns the amount of given seminars per week.

        Returns:
            int: amount of given seminars per week
        """
        return self.n_seminar


    def get_n_practicum(self) -> int:
        """
        Returns the amount of given practica per week.

        Returns:
            int: amount of given practica per week
        """
        return self.n_practica


    def get_time_table(self) -> list:
        """
        Returns timetable of a student.

        Returns:
            list: timetable of a student for one week
        """
        return self._time_table


    def get_enrol_students(self) -> list:
        """
        Returns the enrolled students for a course.

        Returns:
            list: enrolled students
        """
        return self._enrolled_students


    def get_n_enrol_students(self) -> int:
        """
        Returns the amount of enrolled students for a course

        Returns:
            int: amount of enrolled students
        """
        return len(self._enrolled_students)


    def get_groups_per_seminar(self) -> int:
        """
        Returns the amount of groups to be scheduled per seminar.

        Returns:
            int: amount of groups
        """
        return self._groups_per_seminar


    def get_stud_per_sem_group(self) -> int:
        """
        Returns the number of students per seminar group.

        Returns:
            int: number of students
        """
        return self._students_per_sem_group


    def get_seminar_groups(self) -> list:
        """
        Returns a list containing containing groups. Each group represents a list
        containing the students in their respective groups.

        Returns:
            list: groups of students per seminar
        """
        return self._seminar_groups


    def get_groups_per_practicum(self) -> int:
        """
        Returns the amount of groups to be scheduled per practicum.

        Returns:
            int: amount of groups
        """
        return self._groups_per_practicum


    def get_stud_per_prac_group(self) -> int:
        """
        Returns the number of students per praticum group.

        Returns:
            int: number of students
        """
        return self._students_per_prac_group


    def get_practicum_groups(self) -> list:
        """
        Returns a list containing containing groups. Each group represents a list
        containing the students in their respective groups.

        Returns:
            list: groups of students per practica
        """
        return self._prac_groups


    def __repr__(self) -> str:
        return f"{self._abbreviation}, {self.get_n_enrol_students()}"

    def __eq__(self, __o: "Course") -> bool:
        return self._abbreviation == __o._abbreviation
