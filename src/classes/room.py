class Room:
    """
    A class Room representing a room-object for a room in which a course can be scheduled.

    ...

    Attributes
    ----------
    self._room_number (str) = number of the room in the format of a string
    self._capacity (int) = maximum capacity of the number of students that can fit in a room

    Methods
    ----------
    get_time_table(self) -> int
    get_capacity(self) -> int

    """	
    def __init__(self, roomnumber, capacity):
        self._room_number = roomnumber
        self._capacity = capacity

        # Create 2D list representing course time table, each element of the list
        # contains a tuple with the course and a list of students.
        self._time_table = [["-"] * 5 for i in range(5)]


    def get_time_table(self) -> list:
        """
        Returns the time table of the room.

        Returns:
            list: the time table of the room
        """
        return self._time_table


    def get_capacity(self) -> int:
        """
        Returns the maximum capacity of a room.

        Returns:
            int: maximum capacity
        """
        return self._capacity


    def __repr__(self) -> str:
        return f"{self._room_number}"
