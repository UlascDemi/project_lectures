# Classes file




class Student:

    def __init__(self, lastname, surname, studentnumber, course1, course2, course3, course4, course5):
        self._lastname = lastname
        self._surname = surname
        self._studentnumber = studentnumber
        self._course1 = course1
        self._course2 = course2
        self._course3 = course3
        self._course4 = course4
        self._course5 = course5


class Rooms:
    
    def __init__(self, roomnumber, capacity):
        self._roomnumber = roomnumber
        self._capacity = capacity


class Courses:
    def __init__(self, vak, hoorcollege, werkcollege, max_students_werk, practica, max_students_prac, verwacht):
        self._course = vak
        self._lecture = hoorcollege
        self._worklecture = werkcollege
        self._max_students_work = max_students_werk
        self._practica = practica
        self._max_students_prac = max_students_prac
        self._expected_students = verwacht
