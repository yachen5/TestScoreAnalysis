import numpy as np
import pandas as pd
import plotly_express as px


def top_error_questions(group):
    return group.nlargest(5, 'Percentage')


class Subject:
    def __init__(self, df):
        self.error_rank = None
        self.r_text = None
        self.idv_score = None
        self.df = df
        self.question_count = len(list(self.df['Question'].unique()))
        self.student_scores()
        self.error_rank_by_student_top5()

    def student_scores(self):
        # Group by to get % correct by student
        s_df = self.df.groupby(['學號', 'Answer']).agg({'Question': 'count'})
        s_df['Percentage'] = s_df.groupby(['學號'])['Question'].transform(lambda x: x / x.sum())
        s_df = s_df.reset_index()
        s_df['percentage_text'] = s_df['Percentage'].apply(lambda x: f'{int(x * 100)}%')
        s_c = s_df[s_df['Answer'] == '.']
        self.idv_score = s_c.copy()
        s_c = s_c.sort_values(by='Percentage', ascending=True)

    def error_rank_by_student_top5(self):
        df = self.df[self.df['Answer'] != '.'].copy()
        correct_all = self.correct_rate([''], True)
        df_m = df.merge(correct_all, on=['Question'], how='left')
        # print(df_m.columns)
        # 暫時不Rank 全部都列入
        #                 df_g = df_m.groupby('學號').apply(top_error_questions)
        #                 # print(df_g)
        #                 # use drop = True because the above apply method maintain the 學號 column. This is to avoid error
        #                 df_g = df_g.reset_index(drop=True)
        self.error_rank = df_m.copy()

    def correct_rate(self, id_list, exclude=True):
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
        df_a = df_1[df_1['Answer'] == '.'].copy()
        df_a = df_a.drop(columns=['年級', '學號', 'Answer'])
        return df_a
        # # df_1 = df_1.sort_values(by='Answer')
        # category_order = list(df_1['Question'].unique()).sort()
        # fig = px.bar(df_1, x='Question', y='Percentage', color='Answer', text='percentage_text', facet_row='年級',
        #              width=1200, height=600, category_orders={'Question': category_order})
        # st.markdown('### 各題答案分布')
        # st.markdown("\t .\t-----> 回答正確")
        # st.markdown("\t =\t-----> 空白未作答")
        # st.plotly_chart(fig)
        # df_a = df_1[df_1['Answer'] == '.'].copy()
        # df_a = df_a.drop(['學號', 'Answer'], axis=1)
        #
        # df_sorted = df_a.sort_values(by='Percentage')
        #
        # fig = px.bar(df_sorted, x='Question', y='Percentage', text='percentage_text', color='Percentage', width=1200,
        #              height=600, color_continuous_scale=["red", "green"])
        # st.markdown('### 各題 依答對率排序')
        # st.plotly_chart(fig)
        # return df_sorted

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
        df = df[['班級', '座號', '學號']]
        df = df.drop_duplicates(subset=['學號'])
        self.students = df.copy()
        self.class_numbers = list(self.students['學號'].unique())
        self.class_numbers.sort()


def callback_analysis(df, a_q, a_c, col):
    df_q = df[(df['Question'] == a_q) & (df['班級'].isin(a_c))]

    # st.dataframe(df_q)
    grouped_df = df_q.groupby(['Rank', 'Answer']).agg({'學號': 'count'})
    grouped_df['Percentage'] = grouped_df.groupby(['Rank'])['學號'].transform(lambda x: x / x.sum())
    grouped_df = grouped_df.reset_index()
    grouped_df['Percentage'] = grouped_df['Percentage'].fillna(0)
    grouped_df['percentage_text'] = grouped_df['Percentage'].apply(lambda x: f'{int(x * 100)}%')
    # Display the grouped DataFrame with counts
    # st.dataframe(grouped_df)

    df_p = df_q.copy()
    df_pp = df_p.groupby('Answer').agg({'學號': 'count'})
    df_pp['Percentage'] = df_pp['學號'].transform(lambda x: x / len(df_q))
    df_pp = df_pp.reset_index()
    df_pp['percentage_text'] = df_pp['Percentage'].apply(lambda x: f'{int(x * 100)}%')
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
