import numpy as np


class Student:
    def __init__(
        self, first_name: str, last_name: str, student_num: str, courses: list
    ) -> None:

        self._first_name = first_name
        self._last_name = last_name
        self._student_num = student_num
        self._courses = courses
        self._time_table = np.array((5, 5))  # hierin komt een tuple: (Room, Course)
