from __future__ import annotations

from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room


def reschedule_time_slot(
    course: Course, room_time_slots: list, start_time_slot, end_time_slot
) -> None:
    """
    This functions removes an activity from a timeslot and schedules it in another
    timeslot. It checks the available timeslots after everything course is scheduled.
    When this timeslot is found the content of the original timeslot will be moved to
    this new timeslot. This will be done foor the room, students and course.

    Args:
        course (Course): course object
        room_time_slots (list): list of available timeslots
        start_time_slot (tuple): tuple which contains original room, day and timeslot 
        end_time_slot (tuple)): tuple which contains new room, day and timeslot
    """

    if len(room_time_slots) != 16:
        breakpoint()

    # Unpack the time_slot tuples
    start_room, start_day_i, start_time_slot_i = start_time_slot
    end_room, end_day_i, end_time_slot_i = end_time_slot

    course_time_table = course.get_time_table()

    # Take the contents of the course time slot
    room, students = course_time_table[start_day_i][start_time_slot_i]

    # Remove the old time slot and put contents in new time slot
    course_time_table[start_day_i][start_time_slot_i] = "-"
    course_time_table[end_day_i][end_time_slot_i] = end_room, students

    start_room_time_table = start_room.get_time_table()
    end_room_time_table = end_room.get_time_table()

    # Remove old time slot from the room timetable and put contents in new time slot
    if end_room.get_time_table()[end_day_i][end_time_slot_i] != "-":
        breakpoint()

    start_room_time_table[start_day_i][start_time_slot_i] = "-"
    end_room_time_table[end_day_i][end_time_slot_i] = course, students

    # Go through each student, remove the old time slot and put contents in new time slot
    for student in students:
        student_time_table = student.get_time_table()
        student_start_time_slot = student_time_table[start_day_i][start_time_slot_i]

        # Find correct activity and remove it from the time slot
        for activity in student_start_time_slot:
            scheduled_room = activity[0]
            type = activity[2]

            if scheduled_room == room:
                student_start_time_slot.remove(activity)

        # Append the activty to the new time_slot
        student_new_time_slot = student_time_table[end_day_i][end_time_slot_i]
        student_new_time_slot.append((end_room, course, type))

    room_time_slots.append(start_time_slot)
    room_time_slots.remove(end_time_slot)
