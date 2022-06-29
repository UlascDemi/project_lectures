# Lectures & Class schedules

This code was written to solve a complex problem regarding lecture timetables. In this case, a full week schedule must be created for a number of courses at the Science Park (University of Amsterdam). The courses that need to be scheduled consist of lectures and/or tutorials and/or practicals. For each course there are a number of student registrations available, to be found in the folder `data` in `vakken.csv`. This is the number of students expected. However, seminars and practicals have a maximum number of students that can participate. A lecture lasts 2 hours on a working day. There are a number of time slots available per working day.

The available time-slots are as follows:

- 9:00-11:00
- 11:00-13:00
- 13:00-15:00
- 15:00-17:00
- 17:00-19:00 (This is only available for the largest lecture hall and will however earn minus points).
<p>&nbsp;</p>

In addition, there are also a number of rooms available per day and time slot to schedule lectures. The rooms can be found in `zalen.csv` in the folder `data`. The last time slot on a day (from 17:00-19:00) is only available for the largest lecture hall and results in 5 malus points. The problem this code solves is scheduling all lectures in which students have as few "interlocks" as possible. These are time slots without scheduled activities for the student, but for which and after which an activity does take place. It is important that students have as few interlocks as possible, because this ensures that absences from lectures are lower. Therefore, one interlude for a student on a day will result in one malus point. Two interlocks for a student on one day results in three malus points. Three interlocks in one day for a student is not allowed.
It is essential that all courses be scheduled in the weekly schedule, with a time slot and a room in which all students enrolled in a specific course can participate. If a student has a course conflict, which means the student has two scheduled courses at the same time, this will result in one malus point. The purpose of this code is to create a valid weekly schedule in which the number of malus points is minimized. A valid weekly schedule is a weekly schedule in which all schedulable activities of each course are scheduled with a time slot and a hall. The combination with a hall with a time slot is called a hall slot.

<p>&nbsp;</p>

## Approach to algorithms

---

To understand the approach to algorithms, it is helpful to understand the state-space of the case. There are a total of 39 lectures, 41 working lectures and 49 labs to be scheduled. So this is a total of 129 choices. The number of options for scheduling the courses is (20 time slots \* 7 halls + 5). The plus 5 is for the main hall which has an only evening slot.

Therefore, the size of the state space is $\frac{145!}{(145-129)!}$ = 3,85 \* $10^{238}$.
This is the upper bound of a state space of a valid schedule. Given the large state space, some algorithms are implemented that eventually generate valid weekly grids where the malus points are minimized.

<p>&nbsp;</p>

#### **Algorithm 1. Random Algorithm**

The random algorithm goes through all course objects that need to be scheduled. A course is chosen at random, and then the algorithm looks for an available room with a time slot, based on the capacity of the room and the students enrolled in the course. When a room slot (room with time slot) is found, the course is scheduled in both the student, room, and course weekly schedules. The room is removed from the available rooms list, so it cannot be scheduled again. In this algorithm, the evening slot (for the largest room only) is also available.

<p>&nbsp;</p>

#### **Algorithm 2. Random Algorithm with bias**

This algorithm proceeds in much the same way as the random algorithm without bias. However, there is bias because the algorithm first sorts the list of course objects. The courses are sorted based on their capacity, i.e. the number of students enrolled in each course. Next, the course with the largest capacity is scheduled first. If the course has found a room and time slot that can handle its capacity, then it is scheduled. The room slot (room with time slot) is taken from the available room list. In this algorithm, the evening slot (only for the largest hall) is also available.

<p>&nbsp;</p>

#### **Algorithm 3. Restart Hill Climber Algorithm**

The Hill Climber algorithm starts by choosing a random start state. It then makes a small random adjustment to this state. It moves a box in the schedule to a random other time slot and room that is free. If the state then worsens, when the malus points increase, the adjustment is undone. If the adjustment results in a reduction of malus points, i.e. an improvement, then it leaves the adjustment in place. However, the disadvantage of a Hill Climber algorithm is that it is unclear if you have reached a local optimum, or if it is a global optimum. Therefore, a Restart Hill Climber has been implemented. When the Hill Climber converges 2000 iterations, then another Hill Climber is executed. The Hill Climber then takes a new random starting point and executes everything again.

<p>&nbsp;</p>

#### **Algorithm 4. Simulated Annealing (variant of the Hill Climber).**

The Hill Climber algorithm tend to get easily stuck in a local minimum. Simulated Annealing is an effective solution to this problem. Simulated Annealing uses an acceptance probability instead of accepting an improvement. At the beginning, a higher temperature is used that has a higher acceptance probability and thus accepts deteriorated situations more often. For the further steps, the temperature is gradually lowered so that the acceptance probability for deteriorated situations decreases. In this way, the local minimum in the search space is eliminated and we converge to the global minimum.
In the simulated annealing algorithm, just like the Hill Climber, a random state is chosen. It then randomly moves a box to a randomly available time slot. The adjustment is accepted based on an acceptance probability. It is now possible to schedule adjustments that are a degradation. As the iterations increase, the temperature will decrease. The temperature will cause fewer and fewer deteriorating adaptations to be accepted.

<p>&nbsp;</p>

#### **Algorithm 5. Greedy Algorithm**

The Greedy algorithm is implemented based on the heuristics to reduce the number of conflicts. The algorithm takes the sorted list of courses to be scheduled. From this, a course is chosen and the algorithm looks for the time slots that has the most halls available. It then chooses a room that matches the capacity of the course. So if a course has 20 students, it will choose a room that has a capacity of 20 or for example 22. In this way the algorithm always chooses the best option for scheduling the courses.

<p>&nbsp;</p>

## Gettings Started

---

### **_Prerequisites_**

To get started with this codebase, it is a requirement to work with Python3.8. The requirements.txt contains all the packages needed to run the code successfully. This needs to be installed via pip in the terminal. You need to install it with the following instructions:

```
Pip install -r requirements.txt
```

<p>&nbsp;</p>

### **_Structure_**

The repository contains a the following folders:

- In the `data`- folder are the csv files with essential data to build the grid.
- In the `docs`- folder are the visualizations in png files of the algorithms.
- In the `output`- folder is the csv-file with the final result when the code is executed.
- The `src`- folder contains all the python code needed to run the program. This includes the files for the algorithms, the files for the classes, the file that calculates the malus points and a file that checks the validity of the roster.

<p>&nbsp;</p>

### **_Testing_**

To run the code with the default configuration use the following instruction:

```
Python3 main.py
```

<p>&nbsp;</p>

### **_Authors_**

- Justin Uiterloo
- Ulas Demirtas
- Brechje Seegers

<p>&nbsp;</p>

### **_Acknowledgements_**

During an intensive period of six months we gained all the knowledge to finally be able to write this program. It was an instructive period in which we not only learned how to write a program in python, but also how to reflect on our work and improve it. Therefore, we would like to thank the teachers of the programming minor. First, we would like to thank the coordinator of the minor, _Martijn Stegeman_. In addition, we would like to thank the teachers for their good supervision, patience and transfer of knowledge. These are _Jelle van Assema_, _Bas Terwijn_, _Dr. Ing. Anuj Pathania_ and _Wouter Vrielink_. Our next thanks go to the two teaching assistants who provided us with continuous feedback throughout this project to keep us on track. Their feedback gave us many insights into how best to approach problems and especially how to generate and present results in a scientific way. In addition to their knowledge, we would like to thank them for their fine cooperation. These are _Marijn Doeve_ and _Pamela Sneeks_.

Last but not least we could not move forward because of the experience and knowledge of all the instructors. With their feedback and help we gained a lot of knowledge in dealing with problems, debugging and background information about software. We would therefore like to thank _Joos Akkerman, Mayla Kersten, Alwan Rashid_ and _Quinten van der Post_.
