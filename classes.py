# Classes file


class Student:
    def __init__(
        self, first_name: str, last_name: str, student_num: str, courses: list
    ) -> None:

        self._first_name = first_name
        self._last_name = last_name
        self._studentnumber = student_num
        self._courses = courses


class Room:
    def __init__(self, roomnumber, capacity):
        self._roomnumber = roomnumber
        self._capacity = capacity


class Course:
    def __init__(
        self,
        vak,
        hoorcollege,
        werkcollege,
        max_students_werk,
        practica,
        max_students_prac,
        verwacht,
    ):
        self._course = vak
        self._lecture = hoorcollege
        self._worklecture = werkcollege
        self._max_students_work = max_students_werk
        self._practica = practica
        self._max_students_prac = max_students_prac
        self._expected_students = verwacht
