import pandas as pd
from typing import Dict, Any

class ClassGroup:
    """A class representing a group of students in a specific year.

    Attributes:
        df (pd.DataFrame): The DataFrame containing student data.
        name (int): The year of the class group.
        classes (pd.Series): Unique classes in the group.
        student_numbers (pd.DataFrame): Student IDs.
        subjects (pd.Series): Subjects available for this group.
    """

    def __init__(self, df: pd.DataFrame, a_year: int):
        self.name: int = a_year
        self.df: pd.DataFrame = df.copy()
        self.classes = self.df['班級'].unique()
        student_numbers = self.df['學號'].unique()
        # convert self.student_numbers to a dataframe
        self.student_numbers = pd.DataFrame(student_numbers, columns=['學號'])
        self.subjects = self.df['年級_科目'].unique()

    # from the subject class, each subject have calculated the PW column
    # try to assign it to each student number
    def add_pw_by_subject(self, result_dict: Dict[str, Any]):

        """Adds PW (Performance Weight?) scores for each subject to the student numbers dataframe."""
        for subject_l in self.subjects:
            if subject_l in result_dict:
                a_subject = result_dict[subject_l]

                # given a subject class
                # create a single column dataframe that use subject_name as column name and PW as data
                df = self.student_numbers.merge(a_subject.idv_score[['學號', 'PW']], on=['學號'], how='left').copy()
                # Rename PW to the subject name
                self.student_numbers = df.rename(columns={'PW': a_subject.name}).copy()

    # use student_numbers to find the student's class
    # create a dataframe with only student numbers and class
    def get_student_class_df(self):
        df = self.df[['學號', '班級']]
        df = df.drop_duplicates(subset=['學號'])
        return df.copy()
