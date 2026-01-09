import pandas as pd
from typing import Optional, List
from icecream import ic
from src.analysis import statistics

class Subject:
    """A class representing a subject.

    Attributes:
        name (str): The name of the subject.
        df (pd.DataFrame): Input data for the subject.
        question_count (int): Number of unique questions.
        idv_score (Optional[pd.DataFrame]): Individual scores per student.
        correct_rate_all (Optional[pd.DataFrame]): Overall correct rates per question.
        error_rank (Optional[pd.DataFrame]): Error ranking data.
        distinguish_rate (Optional[pd.DataFrame]): Discrimination index data.
        large_df (Optional[pd.DataFrame]): Merged dataframe with scores.
    """

    def __init__(self, df: pd.DataFrame, name: str):
        """Initialize the Subject class.

        Args:
            df (pd.DataFrame): A DataFrame containing the input data.
            name (str): The name of the subject.
        """
        self.name: str = name
        self.df: pd.DataFrame = df
        self.large_df: Optional[pd.DataFrame] = None
        self.q_by_answer: Optional[pd.DataFrame] = None
        self.distinguish_rate: Optional[pd.DataFrame] = None
        self.error_rank: Optional[pd.DataFrame] = None
        self.r_text: Optional[str] = None
        self.idv_score: Optional[pd.DataFrame] = None
        
        # Calculate the number of unique questions in the input data
        self.question_count: int = len(list(self.df['Question'].unique()))

        # Initialize student scores
        self.student_scores()
        # Calculate the overall correct rate, excluding specific conditions
        self.correct_rate_all = self.correct_rate([''], exclude=True)
        # Calculate the error ranking by student for all students
        self.calculate_error_rank_by_student_all()
        # Calculate the discrimination index
        self.get_distinguish_rate()

    # divide the students into 10 groups based on scores and assign a score to each student
    # the lowest group is assign the number 0.1, the highest group is assign the number 1

    def student_scores(self):
        """Calculate the scores of each student."""
        ic.disable()
        # score of each student (by id)
        s_df = statistics.calculate_percentage(self.df, ['學號'], 'Answer', 'Question')
        s_c = s_df[s_df['Answer'] == '.'].copy()
        s_c = s_c.drop(columns=['Answer', 'Question'])
        ic(s_c)
        # assign each student to a group
        # add PG column to the dataframe
        s_c = statistics.assign_four_groups(s_c)
        # add PW column to the dataframe
        s_c = statistics.assign_ten_groups(s_c)

        ic(s_c)
        self.idv_score = s_c.copy()

    def calculate_error_rank_by_student_all(self):
        """Calculate the error rank of each question by student."""

        # Each student answers certain questions incorrectly. Get the correction rate of the whole group and link to
        # the incorrectly answered questions.
        df = self.df[self.df['Answer'] != '.'].copy()
        correct_all = self.correct_rate_all
        df_m = df.merge(correct_all, on=['Question'], how='left')
        self.error_rank = df_m.copy()

    def correct_rate(self, id_list, exclude=True):
        """Calculate the correct rate of each question by a subset of students."""
        # given a set of id, calculate the correct rate of each question done by this subset of students
        # can pass an empty id_list and select exclude =True to get the whole school year
        df = self.df.copy()
        # print(df)
        in_list = df['學號'].isin(id_list)
        if exclude:
            df = df[~in_list]
        else:
            df = df[in_list]

        grouped_df = df.groupby(['年級', 'Question', 'Answer']).agg({'學號': 'count'})
        grouped_df['Percentage'] = grouped_df.groupby(['年級', 'Question'])['學號'].transform(lambda x: x / x.sum())
        grouped_df = grouped_df.reset_index()
        grouped_df['percentage_text'] = grouped_df['Percentage'].apply(lambda x: f'{int(x * 100)}%')
        df_1 = grouped_df.copy()
        self.q_by_answer = df_1.copy()
        df_a = df_1[df_1['Answer'] == '.'].copy()
        df_a = df_a.drop(columns=['年級', '學號', 'Answer'])
        return df_a.copy()

    def get_distinguish_rate(self):
        """Calculate the distinguish rate of each question by group."""

        # each student (idv_score) is assigned a group name H, MH, ML, L
        # get the correct rate of each question and each group
        # use the percentage(correct) of H group - L group to get distinguish rate by question
        ic.disable()
        df = self.df.copy()
        df = df.merge(self.idv_score, on=['學號'], how='left')
        # this is the largest
        self.large_df = df.copy()
        
        df_g = statistics.calculate_percentage(df, ['PG', 'Question'], 'Answer', '學號')

        df_p = df_g[df_g['Answer'] == '.']
        df_p['Percentage'] = round(df_p['Percentage'], 3)
        df_pivot = pd.pivot_table(df_p, values='Percentage', index='Question', columns='PG')
        # Check if columns exist before calculation to be safe
        if 'PH' in df_pivot.columns and 'PL' in df_pivot.columns:
            df_pivot['Delta'] = df_pivot['PH'] - df_pivot['PL']
        else:
            df_pivot['Delta'] = 0
            
        ic(df_pivot)
        df_pivot.reset_index()
        self.distinguish_rate = df_pivot.copy()
        # ic(df)

    def build_question_matrix(self):
        """Builds a question matrix by merging correct rate and distinguish rate dataframes.

        Returns:
            pandas.DataFrame: The question matrix dataframe.
        """
        df_m = self.correct_rate_all.merge(self.distinguish_rate, on=['Question'], how='left')

        threshold_high = 0.75
        threshold_medium = 0.5

        # Use np.select to create a new column based on conditions
        df_m['P_Category'] = pd.cut(df_m['Percentage'],
                                    bins=[-float('inf'), threshold_medium, threshold_high, float('inf')],
                                    labels=['L', 'M', 'H'])

        threshold_high = 0.4
        threshold_medium = 0.25

        # Use np.select to create a new column based on conditions
        df_m['D_Category'] = pd.cut(df_m['Delta'], bins=[-float('inf'), threshold_medium, threshold_high, float('inf')],
                                    labels=['L', 'M', 'H'])
        return df_m.copy()
