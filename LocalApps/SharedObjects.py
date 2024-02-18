import numpy as np
import pandas as pd
import plotly_express as px
from icecream import ic


def top_error_questions(group):
    return group.nlargest(5, 'Percentage')


class Subject:
    """A class representing a subject.

    Attributes:
        large_df (DataFrame): A DataFrame containing the merged data.
        q_by_answer (DataFrame): A DataFrame containing the correct rate of each question by answer.
        distinguish_rate (DataFrame): A DataFrame containing the distinguish rate of each question by group.
        error_rank (DataFrame): A DataFrame containing the error rank of each question by student.
        r_text (str): A string representing the description of the R1~R6 grouping.
        idv_score (DataFrame): A DataFrame containing the individual scores of each student.
        df (DataFrame): A DataFrame containing the input data.
        question_count (int): The number of unique questions in the input data.
        correct_rate_all (DataFrame): A DataFrame containing the correct rate of all questions.
    """

    def __init__(self, df):
        """Initialize the Subject class.

        Args:
            df (DataFrame): A DataFrame containing the input data.
        """
        self.large_df = None
        self.q_by_answer = None
        self.distinguish_rate = None
        self.error_rank = None
        self.r_text = None
        self.idv_score = None
        self.df = df
        self.question_count = len(list(self.df['Question'].unique()))
        self.student_scores()
        self.correct_rate_all = self.correct_rate([''], exclude=True)
        self.calculate_error_rank_by_student_all()
        self.get_distinguish_rate()

    def student_scores(self):
        """Calculate the scores of each student."""
        ic.disable()
        # score of each student (by id)
        # Group by to get % correct by student
        s_df = self.df.groupby(['學號', 'Answer']).agg({'Question': 'count'})
        s_df['Percentage'] = s_df.groupby(['學號'])['Question'].transform(lambda x: x / x.sum())
        s_df = s_df.reset_index()
        s_df['percentage_text'] = s_df['Percentage'].apply(lambda x: f'{int(x * 100)}%')
        s_c = s_df[s_df['Answer'] == '.']
        s_c = s_c.drop(columns=['Answer', 'Question'])
        ic(s_c)
        # assign each student to a group
        s_c = assign_four_groups(s_c)
        ic(s_c)
        self.idv_score = s_c.copy()

    def calculate_error_rank_by_student_all(self):
        """Calculate the error rank of each question by student."""

        # Each student answers certain questions incorrectly. Get the correction rate of the whole group and link to
        # the incorrectly answered questions.
        df = self.df[self.df['Answer'] != '.'].copy()
        correct_all = self.correct_rate_all
        df_m = df.merge(correct_all, on=['Question'], how='left')
        # print(df_m.columns)
        # 暫時不Rank 全部都列入
        #                 df_g = df_m.groupby('學號').apply(top_error_questions)
        #                 # print(df_g)
        #                 # use drop = True because the above apply method maintain the 學號 column. This is to avoid error
        #                 df_g = df_g.reset_index(drop=True)
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
        #
        # df_g = df.groupby(['PG', 'Question', 'Answer']).agg({'學號': 'count'})
        # df_g['Percentage'] = df_g.groupby(['PG', 'Question'])['學號'].transform(lambda x: x / x.sum())
        # df_g = df_g.reset_index()
        df_g = calculate_percentage(df, ['PG', 'Question'], 'Answer', '學號')

        df_p = df_g[df_g['Answer'] == '.']
        df_p['Percentage'] = round(df_p['Percentage'], 3)
        df_pivot = pd.pivot_table(df_p, values='Percentage', index='Question', columns='PG')
        df_pivot['Delta'] = df_pivot['PH'] - df_pivot['PL']
        ic(df_pivot)
        df_pivot.reset_index()
        self.distinguish_rate = df_pivot.copy()
        # ic(df)

    def build_question_matrix(self):
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


class Class:
    def __init__(self, df):
        # df2 = df.copy()
        self.subjects = list(df['年級_科目'].unique())
        df = df[['班級', '座號', '學號']]
        df = df.drop_duplicates(subset=['學號'])
        self.students = df.copy()
        self.class_numbers = list(self.students['學號'].unique())
        self.class_numbers.sort()


def callback_analysis(df, a_q, a_c, col):
    df_q = df[(df['Question'] == a_q) & (df['班級'].isin(a_c))]

    # st.dataframe(df_q)
    grouped_df = calculate_percentage(df_q, ['Rank'], 'Answer', '學號')

    df_p = df_q.copy()

    df_pp = calculate_percentage(df_p, [], 'Answer', '學號')

    df_pp = df_pp.sort_values(by='Answer')

    # get correct
    cor_p = df_pp.copy()
    cor_p = cor_p.set_index('Answer')
    cp_value = cor_p.loc['.', 'percentage_text']
    col.markdown(f'此組分類正確率:{cp_value}')

    col.markdown(f"{a_c} 分群組答對率")
    fig = px.bar(grouped_df, x='Rank', y='Percentage', color='Answer', text='percentage_text')
    col.plotly_chart(fig)
    col.markdown(f"{a_c} 答案分布圖")
    fig = px.bar(df_pp, x='Answer', y='Percentage', color='Answer', text='percentage_text')
    col.plotly_chart(fig)


def assign_four_groups(df):
    group_size = len(df) // 4
    df = df.sort_values('Percentage', ascending=True)
    df['PG'] = pd.cut(np.arange(len(df)),
                      bins=[-1, group_size, 2 * group_size, 3 * group_size, len(df)],
                      labels=['PL', 'PML', 'PMH', 'PH'], include_lowest=True)
    return df.copy()


def dis_index(df):
    df = assign_four_groups(df)
    # st.dataframe(df)
    df_g = df.groupby(['PG', 'Answer']).agg({'學號': 'count'})
    df_g['Percentage'] = df_g.groupby(['PG'])['學號'].transform(lambda x: x / x.sum())
    df_g = df_g.reset_index()
    df_p = df_g[df_g['Answer'] == '.']
    df_p = df_p.set_index('PG')
    ph = round(df_p.loc['PH', 'Percentage'], 3)
    pl = round(df_p.loc['PL', 'Percentage'], 3)
    #
    # st.dataframe(df_p)
    # st.markdown([ph, pl])
    return ph, pl


def calculate_percentage(df, group_cols, by_col, count_col):
    df = df.copy()
    df = df.groupby(group_cols + [by_col]).agg({count_col: 'count'})
    if len(group_cols) == 0:
        df['Percentage'] = df[count_col].transform(lambda x: x / len(df))
    else:
        df['Percentage'] = df.groupby(group_cols)[count_col].transform(lambda x: x / x.sum())
    df['Percentage'] = df['Percentage'].fillna(0)
    df = df.reset_index()
    df['percentage_text'] = df['Percentage'].apply(lambda x: f'{int(x * 100)}%')
    return df
