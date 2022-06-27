from __future__ import annotations
from src.algorithm.hillclimber import reschedule_time_slot
from src.classes.student import Student
from src.classes.course import Course
from src.classes.room import Room
from src.algorithm.Completely_random import random_schedule_course
from src.algorithm.random_scheduling import get_choosable_rooms

import random

from src.malus_point_count.malus_point_count import malus_point_count

# Kiest geen random optie: telkens de beste
# Loop door courses: plant de course in en berekent voor alle mogelijkheden
# de maluspunten. Wanneer de maluspunten het laagst zijn plant hij hem def in

# Letten op: random bv op basis van veel maluspunten uit random. 
# available_rooms: 
# Slide maken waarom je greedy op welk probleem: werkte wel of niet

def greedy(courses_sorted, available_rooms: list[Room]):

    for course in courses_sorted:
        schedule_lecture(course, available_rooms)

    #print(courses_sorted[0])
    # Loop door de courses:
    # for course in courses_sorted:
        
    #     # plan course in
    #     schedule_course(course, available_rooms)

    #     maluspunten = malus_point_count(students, rooms)
    #     if maluspunten == 0:
    #          schedule_course(course, available_rooms)
    #     else:
    #         for timeslot in available_rooms:
    #             reschedule_time_slot
    

def schedule_lecture(course: Course, available_rooms: list[Room]):
    
    for _ in range(course.n_lecture):
        # Checks if lectures need to be given
        if course.n_lecture == 0:
            return True
        
        minimum_cap = course.get_n_enrol_students()

        choosable_rooms = get_choosable_rooms(available_rooms, minimum_cap)

        if len(choosable_rooms) == 0:
            return False
        
        print(choosable_rooms)
        
        # Loop door elke mogelijke room
        # Schedule die optie 
        # Sla maluspunten op voor die keuze
        # tupel: maluspunten, tijdslot
        # Als maluspunten laagst zijn, plan in, en volgende 

        for room in choosable_rooms:
            zaal = room[0]
            day = room[1]
            time_slot = room[2]

            course_time_table = course.get_time_table()
            room_time_table = room.get_time_table()

            # Update time tables
            course_time_table[day][time_slot] = zaal, course.get_enrol_students()
            room_time_table[day][time_slot] = course, course.get_enrol_students()

            # Update time tables for all students
            for student in course.get_enrol_students():
                student_time_table = student.get_time_table()

                student_time_table[day][time_slot].append((zaal, course, "Lec"))
            
            malus_points = malus_point_count(students, rooms)

            # sla mogelijkheid op een een datastructure van maluspunten, met tijdslot 

            # verwijder weer uit schedule
            # forloop opnieuw
            





        


