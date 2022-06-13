import numpy as np
from math import ceil


class Room:
    def __init__(self, roomnumber, capacity):
        self._room_number = roomnumber
        self._capacity = capacity

        # hierin komt een tuple: (lijst[student_num], Course)
        self._time_table = [["-"] * 5 for i in range(5)]

    def get_time_table(self) -> list:
        """
        Returns the time table of the room

        Returns:
            list: the time table of the room
        """
        return self._time_table

    def get_capacity(self) -> int:
        return self._capacity

    def __repr__(self) -> str:
        return f"{self._room_number}"
