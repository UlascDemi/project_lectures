
# Dit zou 1 maluspunt moeten zijn
time_table_1 = [
    [[1],[1],[],[1],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]]
]


# Dit zou 3 maluspunten moeten zijn
time_table_2 = [
    [[],[],[],[],[]],
    [[],[1],[],[],[1]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]]
]

# Dit zou 5 maluspunten moeten zijn
time_table_3 = [
    [[],[],[],[],[]],
    [[],[],[],[],[1]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]]
]

# Dit zou 1 maluspunten moeten zijn
time_table_4 = [
    [[],[1,1],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]]
]

# schedule validity is false 
time_table_5 = [
    [[1],[],[],[],[1]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]]
]

# schedule validity id false 
time_table_6 = [
    [[1],[],[],[],[1]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]]
]

def tussenuur_count(students) -> int:
    tussen_uur_maluspunt = 0

    # for student in students:
    for day in students:
        activiteit = 0
        first_activity = None
        last_activity = None

        for i, time_slot in enumerate(day):
            if len(time_slot) != 0:
                if activiteit == 0:
                    first_activity = i
                activiteit += 1
                last_activity = i
        
        if first_activity != last_activity:    
            amount_activities = last_activity - first_activity +1
            tussen_uren = amount_activities - activiteit

            if tussen_uren == 1:
                tussen_uur_maluspunt += 1
            elif tussen_uren == 2:
                tussen_uur_maluspunt += 3
            elif tussen_uren > 2:
                print("ERROR: more than two free periods")

    return tussen_uur_maluspunt

print(tussenuur_count(time_table_1))
print(tussenuur_count(time_table_2))
print(tussenuur_count(time_table_5))


