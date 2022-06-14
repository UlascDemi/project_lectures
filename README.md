# Lectures & Class schedules

This code was written to solve a complex problem regarding lecture timetables. In this case, a full week schedule must be created for a number of courses at the Science Park (University of Amsterdam). The courses that need to be scheduled consist of lectures and/or seminars and/or practicals. For each course there are a number of student registrations available, to be found in the folder ```data``` in ```vakken.csv```. This is the number of students expected. However, seminars and practicums have a maximum number of students that can participate. A lecture lasts 2 hours on a working day. There are a number of time-slots available per working day.

The available time-slots are as follows:
- 9:00-11:00
- 11:00-13:00
- 13:00-15:00
- 15:00-17:00
- 17:00-19:00 (This is only available for the largest lecture hall and will however earn minus points).
<p>&nbsp;</p>

In addition, there are also a number of rooms available per day and time slot to schedule lectures. The rooms can be found in ```zalen.csv``` in the folder ```data```. The last time-slot on a day (from 17:00-19:00) is only available for the largest lecture hall and results in malus points. The problem this code solves is scheduling all lectures in which students have as few "intermediate slots" as possible. These are time slots without scheduled activities for the student, but for which and after which an activity does take place. It is important that students have as few interlocks as possible, because this ensures that absences from lectures are lower. Therefore, one interlude for a student on a day will result in one malus point. Two interlocks for a student on one day results in three malus points. Three interlocks in one day for a student is not allowed. 
It is essential that all courses be scheduled in the weekly schedule, with a time slot and a room in which all students enrolled in a specific course can participate. If a student has a course conflict, which means the student has two scheduled courses at the same time, this will result in one malus point.  The purpose of this code is to create a weekly schedule that minimizes the number of malus points.

<p>&nbsp;</p>

## Gettings Started
---------------------

### Prerequisites

To get started with this codebase, it is a requirement to work with Python3.8. The requirements.txt contains all the packages needed to run the code successfully. This needs to be installed via pip in the terminal. You need to install it with the following instructions:
```
Pip install -r requirements.txt
```

<p>&nbsp;</p>

### Structure

The ```data```- folder contains the csv-files with the essential data for setting up the schedule. The data is read by ```loader.py```. 

The ```src```-folder contains all the python code for the program. 

- AFMAKEN

<p>&nbsp;</p>

### Testing

To run the code with the default configuration use the following instruction:

```
Python3 main.py ??? (CHECK)
```

<p>&nbsp;</p>

### Approach algorithms

Nog invullen

<p>&nbsp;</p>

### Authors

- Justin Uiterloo
- Ulas Demirtas
- Brechje Seegers

<p>&nbsp;</p>


### Acknowledgements


