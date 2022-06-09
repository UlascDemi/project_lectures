import numpy as np
from math import ceil


class Room:
    def __init__(self, roomnumber, capacity):
        self._roomnumber = roomnumber
        self._capacity = capacity

        # hierin komt een tuple: (lijst[student_num], Course)
        self._timetable = np.array([5, 5])
