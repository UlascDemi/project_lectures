class Student:
    def __init__(
        self, last_name: str, first_name: str, student_num: str, courses: list
    ) -> None:
        self._first_name = first_name
        self._last_name = last_name
        self._student_num = student_num
        self._courses = courses

        # Create 2D list representing student time table, each element of the list 
        # contains a tuple with the room and the course
        self._time_table = [[[] for _ in range(5)] for _ in range(5)]


    def get_first_name(self) -> str:
        """
        Returns first name of a student

        Returns:
            str: the first name of the student
        """
        return self._first_name

    def get_last_name(self) -> str:
        """
        Returns last name of a student

        Returns:
            str: the last name of the student
        """
        return self._last_name

    def get_student_number(self) -> str:
        """
        Returns studentnumber of a student

        Returns:
            str: the studentnumber of the student
        """
        return self._student_num

    def get_students_courses(self) -> list:
        """
        Returns applied courses of a student

        Returns:
            list: the applied courses of the student
        """
        return self._courses

    def get_time_table(self) -> list:
        """
        Returns timetable of a student

        Returns:
            list : the first name of the student
        """
        return self._time_table

    def __str__(self) -> str:
        return f"{self._first_name} {self._last_name}, {self._student_num}"

    def __repr__(self) -> str:
        return f"({self.__str__()})"
