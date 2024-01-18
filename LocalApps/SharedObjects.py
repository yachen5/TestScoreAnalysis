import numpy as np
import pandas as pd


class Subject:
    def __init__(self, df):
        self.r_text = None
        self.idv_score = None
        self.df = df
        self.question_count = len(list(self.df['Question'].unique()))
        self.student_scores()

    def student_scores(self):
        # Group by to get % correct by student
        s_df = self.df.groupby(['學號', 'Answer']).agg({'Question': 'count'})
        s_df['Percentage'] = s_df.groupby(['學號'])['Question'].transform(lambda x: x / x.sum())
        s_df = s_df.reset_index()
        s_df['percentage_text'] = s_df['Percentage'].apply(lambda x: f'{int(x * 100)}%')
        s_c = s_df[s_df['Answer'] == '.']
        self.idv_score = s_c.copy()
        s_c = s_c.sort_values(by='Percentage', ascending=True)

    def grouping_1(self):
        s_c = self.idv_score.copy()
        group_size = len(s_c) // 6
        s_c['Rank'] = pd.cut(np.arange(len(s_c)),
                             bins=[-1, group_size, 2 * group_size, 3 * group_size, 4 * group_size, 5 * group_size,
                                   len(s_c)],
                             labels=['R1', 'R2', 'R3', 'R4', 'R5', 'R6'], include_lowest=True)
        self.r_text = """### R1~R6 分群曲線
        - 先把全年級學生當科答對率(1=100%)，從最低排到最高
        - 每根bar代表一位學生，移除學號
        - 分成六等分: R1是最高分的一組，到R6是最低分的一組"""

        self.idv_score = s_c.copy()
        #
        #
        #
        # s_c = s_c.drop(['Answer', 'Question'], axis=1)
        # s_p = s_c.copy()
        # s_p = s_p.reset_index(drop=True)
        # s_avg = s_p.groupby('Rank').agg({'Percentage': 'mean'})
        # s_avg = s_avg.reset_index()
        # s_avg['percentage_text'] = s_avg['Percentage'].apply(lambda x: f'{int(x * 100)}%')
        # fig = px.line(s_avg, x='Rank', y='Percentage', text='percentage_text')
        # fig.update_traces(textposition='top center')
        # # Set y-axis to start from zero
        # fig.update_layout(yaxis=dict(range=[0, max(s_avg['Percentage'] + 0.2)]))
        # r_text2 = "各組平均答對率 斜率圖(各組變化太大須注意)"
        # return s_c.copy(), r_text, s_p, fig, r_text2


class Class:
    def __init__(self, df):
        # df2 = df.copy()
        self.subjects = list(df['年級_科目'].unique())
        df = df[['班級', '座號', '姓名', '性別', '學號']]
        df = df.drop_duplicates(subset=['學號'])
        self.students = df.copy()
        self.class_numbers = list(self.students['學號'].unique())
