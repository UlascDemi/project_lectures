from src.loader.loader_pandas import load_students, load_rooms, load_courses

import pandas as pd


def main():

    students = load_students(pd.read_csv("data/studenten_en_vakken.csv"))
    rooms = load_rooms(pd.read_csv("data/zalen.csv"))
    courses = load_courses(pd.read_csv("data/vakken.csv"))

    # print(students)


if __name__ == "__main__":
    main()
