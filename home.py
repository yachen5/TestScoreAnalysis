# This is a sample Python script.
import pickle

import numpy as np
import pandas as pd
import plotly_express as px
import streamlit as st

st.set_page_config(layout="wide")

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Specify the path to your .pkl file
pkl_file_path = r'summary.pkl'


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

    col.markdown(f"{a_c} R1~R6 答對率")
    fig = px.bar(grouped_df, x='Rank', y='Percentage', color='Answer', text='percentage_text')
    col.plotly_chart(fig)
    col.markdown(f"{a_c} 答案分布圖")
    fig = px.bar(df_pp, x='Answer', y='Percentage', color='Answer', text='percentage_text')
    col.plotly_chart(fig)


def layout_part_3(df, df_sorted):
    st.markdown("## 單一問題分析")

    # Add form components
    qs = list(df_sorted['Question'].unique())

    # qs.sort()
    a_q = st.selectbox('請選擇一個題目', qs)

    # specific question's correct % of the whole class year
    all_p = df_sorted.set_index('Question').loc[a_q, 'percentage_text']
    df_qq = df[(df['Question'] == a_q)].copy()
    gg = df_qq.groupby(['班級', 'Answer']).agg({'學號': 'count'})
    gg['Percentage'] = gg.groupby(['班級'])['學號'].transform(lambda x: x / x.sum())
    gg = gg.reset_index()
    gg['percentage_text'] = gg['Percentage'].apply(lambda x: f'{int(x * 100)}%')

    fig = px.bar(gg, x='班級', y='Percentage', color='Answer', text='percentage_text', width=1200, height=600)
    # st.markdown('全年級各班答對比例')
    st.markdown("### 全年級各班答案分布圖")
    st.markdown("\t .\t-----> 回答正確")
    st.markdown("\t =\t-----> 空白未作答")

    st.plotly_chart(fig)

    st.markdown("### 分組比較: 可全年級，幾個班或一個班互比")
    col1, col2 = st.columns(2)
    cc = list(df['班級'].unique())
    cc.sort()
    a_c1 = col1.multiselect('選擇班級，可複選', cc, cc)
    a_c2 = col2.multiselect('選擇班級，可複選', cc, cc[0])

    # Display the entered values after form submission
    if (len(a_c1) > 0) & (len(a_c2) > 0):
        callback_analysis(df, a_q, a_c1, col1)
        callback_analysis(df, a_q, a_c2, col2)


def layout_main(a_dic, a_sel, normal_only):
    if a_sel is not "請選擇":
        df = a_dic[a_sel]
        class_year = df['年級'].iloc[0]
        subj = df['科目代號'].iloc[0]
        # st.dataframe(df)
        st.markdown(f"## {class_year}年級 {subj}科分析")

        # include 體育班 or not
        unique_values = sorted(df['班級'].unique())

        # Step 2: Determine the last unique value
        last_unique_value = unique_values[-1]

        # Step 3: Create a new column 'label' with 'normal' for all rows initially
        df['label'] = 'normal'

        # Step 4: Set 'special' label for rows where the column value is the last unique value
        df.loc[df['班級'] == last_unique_value, 'label'] = 'special'

        if normal_only:
            df = df[df['label'] == 'normal']
        else:
            pass

        # Group by to get % correct by student
        s_df = df.groupby(['學號', 'Answer']).agg({'Question': 'count'})
        s_df['Percentage'] = s_df.groupby(['學號'])['Question'].transform(lambda x: x / x.sum())
        s_df = s_df.reset_index()
        s_df['percentage_text'] = s_df['Percentage'].apply(lambda x: f'{int(x * 100)}%')
        s_c = s_df[s_df['Answer'] == '.'].copy()
        s_c = s_c.sort_values(by='Percentage', ascending=False)

        # Divide students into 6 groups (R1 to R6)
        group_size = len(s_c) // 6
        s_c['Rank'] = pd.cut(np.arange(len(s_c)),
                             bins=[-1, group_size, 2 * group_size, 3 * group_size, 4 * group_size, 5 * group_size,
                                   len(df)],
                             labels=['R1', 'R2', 'R3', 'R4', 'R5', 'R6'], include_lowest=True)

        s_c = s_c.drop(['Answer', 'Question'], axis=1)
        s_p = s_c.copy()
        s_p = s_p.reset_index(drop=True)
        # st.dataframe(s_p)
        st.divider()
        st.markdown("### R1~R6 分群曲線")
        st.markdown("""
        - 先把全年級學生當科答對率(1=100%)，從最高排到最低
        - 每根bar代表一位學生，移除學號
        - 分成六等分: R1是最高分的一組，到R6是最低分的一組""")
        col1, col2 = st.columns(2)
        fig = px.bar(s_p, x=s_p.index, y='Percentage', color='Rank')
        fig.update_xaxes(showticklabels=False)
        col1.markdown('Ranking 排列')
        col1.plotly_chart(fig)
        s_avg = s_p.groupby('Rank').agg({'Percentage': 'mean'})
        s_avg = s_avg.reset_index()
        s_avg['percentage_text'] = s_avg['Percentage'].apply(lambda x: f'{int(x * 100)}%')
        fig = px.line(s_avg, x='Rank', y='Percentage', text='percentage_text')
        fig.update_traces(textposition='top center')
        # Set y-axis to start from zero
        fig.update_layout(yaxis=dict(range=[0, max(s_avg['Percentage'] + 0.2)]))
        col2.markdown('各組平均答對率 斜率圖 (各組變化太大須注意)')
        col2.plotly_chart(fig)

        # join the original data
        b_len = len(df)
        df = df.merge(s_c, on=['學號'], how='left')
        a_len = len(df)

        # to make sure total rows does not increase after merge
        if a_len != b_len:
            st.error('Please check ranking calculation! Unique student id as output')
            st.stop()
        # st.dataframe(df)

        st.divider()
        # Group by to get % correct by question and by the whole class year
        grouped_df = df.groupby(['年級', 'Question', 'Answer']).agg({'學號': 'count'})
        grouped_df['Percentage'] = grouped_df.groupby(['年級', 'Question'])['學號'].transform(lambda x: x / x.sum())
        grouped_df = grouped_df.reset_index()
        grouped_df['percentage_text'] = grouped_df['Percentage'].apply(lambda x: f'{int(x * 100)}%')
        df_1 = grouped_df.copy()
        df_1 = df_1.sort_values(by='Answer')
        fig = px.bar(df_1, x='Question', y='Percentage', color='Answer', text='percentage_text', facet_row='年級',
                     width=1200, height=600)
        st.markdown('### 各題答案分布')
        st.markdown("\t .\t-----> 回答正確")
        st.markdown("\t =\t-----> 空白未作答")
        st.plotly_chart(fig)
        df_a = df_1[df_1['Answer'] == '.'].copy()
        df_a = df_a.drop(['學號', 'Answer'], axis=1)

        df_sorted = df_a.sort_values(by='Percentage')

        fig = px.bar(df_sorted, x='Question', y='Percentage', text='percentage_text', color='Percentage', width=1200,
                     height=600, color_continuous_scale=["red", "green"])
        st.markdown('### 各題 依答對率排序')
        st.plotly_chart(fig)

        st.divider()
        layout_part_3(df, df_sorted)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open(pkl_file_path, 'rb') as pkl_file:
        # Load the data from the Pickle file
        a_dic = pickle.load(pkl_file)

    selections = list(a_dic.keys())
    selections.sort()
    selections.insert(0, "請選擇")
    a_sel = st.sidebar.selectbox("Please select a report", selections)

    n_only = st.sidebar.toggle('普通班分析')
    layout_main(a_dic, a_sel, n_only)
    st.sidebar.write('版本 V3.1203_2023')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
