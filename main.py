from src.loader.loader_pandas import load_students, load_rooms, load_courses

import pandas as pd

# TODO getters voor course schrijven - Brechje
# TODO getters voor room schrijven - Ulas
# TODO getters voor student schrijven - Justin

# TODO docstrings in loader_pandas schrijven


def main():

    students = load_students(pd.read_csv("data/studenten_en_vakken.csv"))
    rooms = load_rooms(pd.read_csv("data/zalen.csv"))
    courses = load_courses(pd.read_csv("data/vakken.csv"))

    total = 0
    for i, (student_num, student) in enumerate(courses.items()):
        total += student._n_lecture

    print(total)


if __name__ == "__main__":
    main()
