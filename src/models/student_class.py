import pandas as pd
from typing import List

class Class:
    """A class representing a group of students in a single class unit.

    Attributes:
        subjects (List[str]): A list of unique subjects in the class.
        students (pd.DataFrame): A DataFrame containing student information.
        student_numbers (List[str]): A sorted list of unique student numbers in the class.
    """

    def __init__(self, df: pd.DataFrame):
        self.subjects: List[str] = list(df['年級_科目'].unique())

        df = df[['班級', '座號', '學號']]
        df = df.drop_duplicates(subset=['學號'])
        self.students = df.copy()
        self.student_numbers = list(self.students['學號'].unique())
        self.student_numbers.sort()
