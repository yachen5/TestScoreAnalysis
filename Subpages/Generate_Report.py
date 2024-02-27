# This is a sample Python script.

import numpy as np
import pandas as pd
import plotly_express as px
import streamlit as st

from LocalApps.SharedLayout import by_class_summary, layout_class
from LocalApps.SharedObjects import callback_analysis, dis_index, calculate_percentage, get_excel_download, \
    convert_stats


def grouping_1(s_c):
    """_summary_

    Args:
        s_c (_type_): _description_

    Returns:
        _type_: _description_
    """
    group_size = len(s_c) // 6
    s_c['Rank'] = pd.cut(np.arange(len(s_c)),
                         bins=[-1, group_size, 2 * group_size, 3 * group_size, 4 * group_size, 5 * group_size,
                               len(s_c)],
                         labels=['R1', 'R2', 'R3', 'R4', 'R5', 'R6'], include_lowest=True)
    r_text = """### R1~R6 分群曲線
    - 先把全年級學生當科答對率(1=100%)，從最低排到最高
    - 每根bar代表一位學生，移除學號
    - 分成六等分: R1是最高分的一組，到R6是最低分的一組"""

    s_c = s_c.drop(['Answer', 'Question'], axis=1)
    s_p = s_c.copy()
    s_p = s_p.reset_index(drop=True)
    s_avg = s_p.groupby('Rank').agg({'Percentage': 'mean'})
    s_avg = s_avg.reset_index()
    s_avg['percentage_text'] = s_avg['Percentage'].apply(lambda x: f'{int(x * 100)}%')
    fig = px.line(s_avg, x='Rank', y='Percentage', text='percentage_text')
    fig.update_traces(textposition='top center')
    # Set y-axis to start from zero
    fig.update_layout(yaxis=dict(range=[0, max(s_avg['Percentage'] + 0.2)]))
    r_text2 = "各組平均答對率 斜率圖(各組變化太大須注意)"
    return s_c.copy(), r_text, s_p, fig, r_text2


def grouping_2(s_c):
    bins_2 = [0, 0.6, 0.7, 0.8, 0.9, 1.1]
    labels_2 = ['<60', '60-69', '70-79', '80-89', '>90']

    s_c, r_text, s_p, fig, r_text2 = ten_group_students(s_c, bins_2, labels_2)

    return s_c.copy(), r_text, s_p, fig, r_text2


def grouping_3(s_c):
    bins_3 = [0, 0.3, 0.6, 0.7, 0.8, 0.9, 1.1]
    labels_3 = ['<30', '30-59', '60-69', '70-79', '80-89', '>90']

    s_c, r_text, s_p, fig, r_text2 = ten_group_students(s_c, bins_3, labels_3)

    return s_c.copy(), r_text, s_p, fig, r_text2


def ten_group_students(s_c, bins, labels, description='Ranking'):
    """
    This function is to group students into 10 groups based on their percentage of the correct answer
    :param s_c: is the dataframe of the students' scores
    :param bins: is the list of the bins
    :param labels: is the list of the labels
    :param description: is the description of the ranking
    :return: a list of items that includes the dataframe of the students' scores, the description of the ranking and the
    figure of the ranking of the students
    """
    s_c['Rank'] = pd.cut(s_c['Percentage'], bins=bins, labels=labels, right=False)
    r_text = f"""### {description}
    - 先把全年級學生當科答對率(1=100%)，從最低排到最高
    - 每根bar代表一位學生，移除學號
    - 分成 {len(labels)} 群: 每10分為一群"""

    s_c = s_c.drop(['Answer', 'Question'], axis=1)
    s_p = s_c.copy()
    s_p = s_p.reset_index(drop=True)
    s_count = s_p.groupby('Rank').agg({'學號': 'count'})
    s_count = s_count.reset_index()
    r_text2 = "各組人數"
    fig = px.bar(s_count, x='Rank', y='學號', text='學號', color='Rank')
    # fig.update_traces(textposition='top center')
    # Set y-axis to start from zero
    # fig.update_layout(yaxis=dict(range=[0, max(s_count['學號'] + 10)]))

    return s_c.copy(), r_text, s_p, fig, r_text2


def layout_part_3(df, df_sorted):
    """

    :param df:
    :param df_sorted: is a dataframe sorted by the percentage of the correct answer
    :return:
    """
    st.markdown("## 單一問題分析")

    # Add form components
    qs = list(df_sorted['Question'].unique())

    # qs.sort()
    a_q = st.selectbox('請選擇一個題目', qs)

    # specific question's correct % of the whole class year
    all_p = df_sorted.set_index('Question').loc[a_q, 'percentage_text']

    df_qq = df[(df['Question'] == a_q)].copy()
    # dis_index(df_qq)
    pa, pb = dis_index(df_qq)
    all_d = round(pa - pb, 3)
    st.markdown(f'### 本題的全年級答對率是{all_p}，鑑別率是{all_d}')
    st.markdown(
        f"""鑑別率(D)計算方法:每25%分成一個群組，D = 最高25%組的達對率{pa} - 最低25%組的答對率{pb}。
        ([參考Link](https://pedia.cloud.edu.tw/Entry/WikiContent?title=%E9%91%91%E5%88%A5%E5%BA%A6&search=%E9%91%91%E5%88%A5%E5%BA%A6) 
        一般而言，鑑別度以0.25以上為標準，高於0.4為優良試題)""")
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


def layout_part_2(df):
    # grouped_df = df.groupby(['年級', 'Question', 'Answer']).agg({'學號': 'count'})
    # grouped_df['Percentage'] = grouped_df.groupby(['年級', 'Question'])['學號'].transform(lambda x: x / x.sum())
    # grouped_df = grouped_df.reset_index()
    grouped_df = calculate_percentage(df, ['年級', 'Question'], 'Answer', '學號')
    df_1 = grouped_df.copy()
    # df_1 = df_1.sort_values(by='Answer')
    category_order = list(df_1['Question'].unique()).sort()
    fig = px.bar(df_1, x='Question', y='Percentage', color='Answer', text='percentage_text', facet_row='年級',
                 width=1200, height=600, category_orders={'Question': category_order})
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
    return df_sorted


def color_based_on_conditions(row):
    if row['P_Category'] == 'L' and row['D_Category'] == 'L':
        return 'purple'
    elif row['P_Category'] == 'L':
        return 'red'
    elif row['P_Category'] == 'L' or row['D_Category'] == 'L':
        return 'yellow'
    else:
        return 'green'


def layout_main(a_dic, a_sel):
    if a_sel != "請選擇":
        a_subject = a_dic[a_sel]
        df = a_subject.df.copy()

        class_year = df['年級'].iloc[0]
        subj = df['科目代號'].iloc[0]
        # # st.dataframe(df)
        st.markdown(f"## {class_year}年級 {subj}科分析")

        fig = by_class_summary(a_subject.df, a_subject.idv_score)
        st.plotly_chart(fig)

        st.markdown('### 各題答對率與鑑別率')
        st.markdown(
            f"""鑑別率(D)計算方法:每25%分成一個群組，D = 最高25%組的達對率 - 最低25%組的答對率。
            ([參考Link](https://pedia.cloud.edu.tw/Entry/WikiContent?title=%E9%91%91%E5%88%A5%E5%BA%A6&search=%E9%91%91%E5%88%A5%E5%BA%A6) 
            一般而言，鑑別度以0.25以上為標準，高於0.4為優良試題)""")
        df_m = a_subject.build_question_matrix()

        df_m['Color'] = df_m.apply(color_based_on_conditions, axis=1)
        df_m = df_m.reset_index(drop=True)
        st.dataframe(df_m)

        df_low = df_m[df_m['Percentage'] < 0.5]
        set1 = set(df_low['Question'].unique())
        st.write(f"題目 {', '.join(df_low['Question'].unique())} 的答對率低於50%")
        df_low2 = df_m[df_m['Delta'] < 0.25]
        set2 = set(df_low2['Question'].unique())
        st.write(f"題目 {', '.join(set2)} 的鑑別率低於25%")
        set3 = set1.intersection(set2)
        list1 = list(set3)
        if len(list1) > 0:
            list1.sort()
            st.write(f"題目 {', '.join(list1)} 的答對率低於50%，且鑑別率低於25%")

        fig = px.scatter(df_m, x='Percentage', y='Delta', title='答對率-鑑別率 Scatter Plot', text='Question',
                         color='Color',
                         color_discrete_map={
                             "purple": 'purple',
                             "red": "red",
                             "yellow": "yellow",
                             "green": "green"},
                         labels={'題目': 'Question', '答對率': 'X-axis', '鑑別率': 'Y-axis'})
        fig.update_traces(textposition='middle right')
        fig.update_xaxes(title_text='答對率')
        fig.update_yaxes(title_text='鑑別率')
        st.plotly_chart(fig)

        df_sorted = df_m.sort_values(by='Percentage')

        fig = px.bar(df_sorted, x='Question', y='Percentage', text='percentage_text', color='Delta',
                     color_continuous_scale=["red", "green"], range_color=[0, 0.8])
        st.markdown("""### 各題 依答對率排序""")

        st.write("""
        Bar越短，答對率越低
        
        顏色越紅，鑑別率越低
        """)

        st.plotly_chart(fig)
        df_low = df_low.sort_values(by='Percentage', ascending=True)
        # df_q = a_subject.q_by_answer.copy()
        large_df = a_subject.large_df.copy()
        # st.dataframe(large_df)
        df_g = large_df.groupby(by=['Question', 'PG', 'Answer']).agg({'學號': 'count'})
        df_g = df_g.reset_index()
        st.markdown('## 單一問題分析 (針對答對率低於50%的題目)')

        for index, row in df_low.iterrows():
            st.write(f'### 本題{row.Question}的答對率為{round(row.Percentage, 3)}，鑑別率為{round(row.Delta, 3)}')
            # st.write(row)
            df_s = df_g[df_g['Question'] == row.Question]
            df_s = df_s.rename(columns={'學號': '人數'})
            # st.dataframe(df_s)
            # st.write(df_s)
            st.markdown("**全年級各分群答案分布圖**")
            st.markdown("""
            **.**-----> 回答正確, **=**-----> 空白未作答
            """)
            st.markdown("PL:低分群 (0%~25%),PML:中低分群(25%~50%),PMH:中高分群(50%~75%),PH:高分群(75%~100%)")
            fig = px.bar(df_s, x='PG', y='人數', color='Answer', text='人數')
            st.plotly_chart(fig)


def main():
    if 'subjects' in st.session_state:
        st.write(
            "主要是提供給科任老師來看學生回答的狀況，從班與班或各個題目的回答狀況來加強某些觀念，也可以進一步研究學生答錯背後的原因")
        a_dic = st.session_state.subjects
        selections = list(a_dic.keys())
        selections.sort()
        selections.insert(0, "請選擇")
        col1, col2, col3 = st.columns(3)
        a_sel = col1.selectbox("Please select a report", selections)

        # g_m = col2.selectbox("選擇分類法", ['一般分法(5組)', '一般分法(6組)', '六等分法'])
        # n_only = col3.toggle('普通班分析')
        # n_only = False
        layout_main(a_dic, a_sel)
    else:
        st.warning("請回到前一步驟，上傳Excel文件")


def by_class_report():
    if 'subjects' in st.session_state:
        st.markdown("主要是提供給導師，在挑選自己的班級後將各科成績分析與班上答題狀況一次呈現。"
                    "另外在本頁最底下有詳列班上學生**不應該答錯的題目**，這部份可以下載Excel File來拆分使用")
        layout_class(include_all=True)
    else:
        st.warning("請回到前一步驟，上傳Excel文件")


def tbd():
    if 'subjects' in st.session_state:
        year_group = st.session_state.year_groups
        s_year = st.selectbox("請選擇年級", list(year_group.keys()))

        # use streamlit to display a text and explain to users about the purpose of this page
        st.markdown("""這分析主要是找出每位學生的各科在全年級的表現級距狀況
        以年級為單位，將每位學生的各科成績按照全年級高低分成十等分，然後計算分數級距從0.1到最高1。藉由統計，找出科目級距的分布狀況，並且給予標籤。
        
        標籤的意義如下：
        - 高低分差距大
        - 平均分數低
        - 各科分數變化大
        - 平均分數高""")

        a_year = year_group[s_year]
        # st.dataframe(a_year.student_numbers)
        # melt the student_numbers dataframe. keep "學號" and move the rest to a new column "科目"
        df_temp = a_year.student_numbers.melt(id_vars=['學號'], var_name='科目', value_name='答對率')
        df_temp['答對率'] = pd.to_numeric(df_temp['答對率'])

        df_temp = df_temp[['學號', '答對率']]
        # st.dataframe(df_temp)
        # df_temp['答對率'] = df_temp['答對率'].apply(lambda x: round(x * 100, 2))
        # calculate the mean and std of the correct rate
        df_g = df_temp.groupby(by='學號')['答對率'].describe()
        df_g = df_g.reset_index()
        # st.dataframe(df_g)
        # find students with max - min >0.5
        df_g['Delta'] = df_g['max'] - df_g['min']
        # add a "tag" column and add "high_delta" tag to indicate if the student has a high delta
        df_g['tag'] = df_g['Delta'].apply(lambda x: '高低分差距大' if x > 0.5 else '')
        # append "low mean" to the tag column if the mean is lower than 0.4. use "," to separate the tags if there are any
        df_g['tag'] = df_g.apply(lambda x: x['tag'] + ',平均分數低' if x['mean'] < 0.4 else x['tag'], axis=1)
        # remove the leading "," if there are any in column tag
        df_g['tag'] = df_g['tag'].apply(lambda x: x.lstrip(','))
        # append "high std" to the tag column if the std is higher than 0.2. use "," to separate the tags if there are any
        df_g['tag'] = df_g.apply(lambda x: x['tag'] + ',各科分數變化大' if x['std'] > 0.2 else x['tag'], axis=1)
        # remove the leading "," if there are any in column tag
        df_g['tag'] = df_g['tag'].apply(lambda x: x.lstrip(','))
        # append "high mean" to the tag column if the mean is higher than 0.7. use "," to separate the tags if there are any
        df_g['tag'] = df_g.apply(lambda x: x['tag'] + ',平均分數高' if x['mean'] > 0.9 else x['tag'], axis=1)
        # remove the leading "," if there are any in column tag
        df_g['tag'] = df_g['tag'].apply(lambda x: x.lstrip(','))

        df_s_class = a_year.get_student_class_df()
        df_g = df_g.merge(df_s_class, on='學號', how='left')
        # students are assigned with various tags
        st.write("學生答題狀況與分析後的標籤")
        # convert english description to chinese
        df_g = convert_stats(df_g)
        st.dataframe(df_g)
        # create a link to download the dataframe as an excel file
        get_excel_download(df_g)


    else:
        st.warning("請回到前一步驟，上傳Excel文件")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # with open(pkl_file_path, 'rb') as pkl_file:
    #     # Load the data from the Pickle file
    #     a_dic = pickle.load(pkl_file)
    main()
    # st.sidebar.write('版本 V1.1222_2023')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
