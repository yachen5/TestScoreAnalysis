# This is a sample Python script.

import numpy as np
import pandas as pd
import plotly_express as px
import streamlit as st

from LocalApps.SharedObjects import callback_analysis, dis_index


# st.set_page_config(layout="wide")


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Specify the path to your .pkl file
# pkl_file_path = r'../summary.pkl'


def grouping_1(s_c):
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
    bins = [0, 0.6, 0.7, 0.8, 0.9, 1.1]
    s_c['Rank'] = pd.cut(s_c['Percentage'], bins=bins,
                         labels=['<60', '60-69', '70-79', '80-89', '>90'], right=False)
    r_text = """### 分群曲線
    - 先把全年級學生當科答對率(1=100%)，從最低排到最高
    - 每根bar代表一位學生，移除學號
    - 分成5群: 每10分為一群"""

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


def grouping_3(s_c):
    bins = [0, 0.3, 0.6, 0.7, 0.8, 0.9, 1.1]
    s_c['Rank'] = pd.cut(s_c['Percentage'], bins=bins,
                         labels=['<30', '30-59', '60-69', '70-79', '80-89', '>90'], right=False)
    r_text = """### 全年級分群曲線
    - 先把全年級學生當科答對率(1=100%)，從最低排到最高
    - 每根bar代表一位學生，移除學號
    - 分成6群: 每10分為一群"""

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
    grouped_df = df.groupby(['年級', 'Question', 'Answer']).agg({'學號': 'count'})
    grouped_df['Percentage'] = grouped_df.groupby(['年級', 'Question'])['學號'].transform(lambda x: x / x.sum())
    grouped_df = grouped_df.reset_index()
    grouped_df['percentage_text'] = grouped_df['Percentage'].apply(lambda x: f'{int(x * 100)}%')
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


def layout_main(a_dic, a_sel):
    if a_sel != "請選擇":
        a_subject = a_dic[a_sel]
        df = a_subject.df.copy()

        class_year = df['年級'].iloc[0]
        subj = df['科目代號'].iloc[0]
        # # st.dataframe(df)
        st.markdown(f"## {class_year}年級 {subj}科分析")

        df_m = a_subject.correct_rate_all.merge(a_subject.distinguish_rate, on=['Question'], how='left')

        st.dataframe(df_m)

        fig = px.scatter(df_m, x='Percentage', y='Delta', title='X-Y Scatter Plot', text='Question',
                         labels={'題目': 'Question', '答對率': 'X-axis', '鑑別率': 'Y-axis'})
        fig.update_traces(textposition='middle right')
        fig.update_xaxes(title_text='答對率')
        fig.update_yaxes(title_text='鑑別率')
        st.plotly_chart(fig)
        #
        # # include 體育班 or not
        # unique_values = sorted(df['班級'].unique())
        #
        # # Step 2: Determine the last unique value
        # last_unique_value = unique_values[-1]
        #
        # # Step 3: Create a new column 'label' with 'normal' for all rows initially
        # df['label'] = 'normal'
        #
        # # Step 4: Set 'special' label for rows where the column value is the last unique value
        # df.loc[df['班級'] == last_unique_value, 'label'] = 'special'
        #
        # if normal_only:
        #     df = df[df['label'] == 'normal']
        # else:
        #     pass
        #
        # # Group by to get % correct by student
        # s_df = df.groupby(['學號', 'Answer']).agg({'Question': 'count'})
        # s_df['Percentage'] = s_df.groupby(['學號'])['Question'].transform(lambda x: x / x.sum())
        # s_df = s_df.reset_index()
        # s_df['percentage_text'] = s_df['Percentage'].apply(lambda x: f'{int(x * 100)}%')
        # s_c = s_df[s_df['Answer'] == '.'].copy()
        # s_c = s_c.sort_values(by='Percentage', ascending=True)
        #
        # # Divide students into 6 groups (R1 to R6)
        # if g_m == '一般分法(5組)':
        #     s_c, a_text, s_p, fig2, a_text2 = grouping_2(s_c)
        # elif g_m == '一般分法(6組)':
        #     s_c, a_text, s_p, fig2, a_text2 = grouping_3(s_c)
        # else:
        #     s_c, a_text, s_p, fig2, a_text2 = grouping_1(s_c)
        #
        # # st.dataframe(s_p)
        # st.divider()
        # st.markdown(a_text)
        # col1, col2 = st.columns(2)
        # fig = px.bar(s_p, x=s_p.index, y='Percentage', color='Rank')
        # fig.update_xaxes(showticklabels=False)
        # col1.markdown('Ranking 排列')
        # col1.plotly_chart(fig)
        #
        # s_minmax = s_p.groupby('Rank')['Percentage'].agg(['min', 'max'])
        # s_minmax = s_minmax.reset_index()
        # st.markdown('各組答對率 [min max] 值')
        # st.dataframe(s_minmax)
        #
        # col2.markdown(a_text2)
        # col2.plotly_chart(fig2)
        #
        # # join the original data
        # b_len = len(df)
        # df = df.merge(s_c, on=['學號'], how='left')
        # a_len = len(df)
        #
        # # to make sure total rows does not increase after merge
        # if a_len != b_len:
        #     st.error('Please check ranking calculation! Unique student id as output')
        #     st.stop()
        # # st.dataframe(df)
        # st.divider()
        # layout_by_class(df, s_c)
        #
        # st.divider()
        # df_sorted = layout_part_2(df)
        # # Group by to get % correct by question and by the whole class year
        #
        # st.divider()
        # layout_part_3(df, df_sorted)
        # st.success("完成!")


def layout_by_class(df, s_c):
    st.markdown('### 各班成績分布與排名')
    col1, col2 = st.columns(2)
    # st.dataframe(df)
    df_box = df.groupby(['班級', '學號'], as_index=False).agg({'Question': 'count'})
    df_box = df_box.merge(s_c, on=['學號'], how='left')
    df_desc = df_box.groupby(['班級'])['Percentage'].describe()
    col1.dataframe(df_desc)
    # Find the top category by mean and median (50%)
    top_categories_mean = df_desc['mean'].nlargest(3).index
    top_categories_median = df_desc['50%'].nlargest(3).index
    # Generate the text summary for mean
    text_summary_mean = f"平均前三名的班級: {', '.join(top_categories_mean)} 各自平均為 {', '.join([f'{mean:.2f}' for mean in df_desc.loc[top_categories_mean, 'mean']])}"
    # Generate the text summary for median (50%)
    text_summary_median = f"中位數前三名的班級: {', '.join(top_categories_median)} 各自中位數為 {', '.join([f'{median:.2f}' for median in df_desc.loc[top_categories_median, '50%']])}"
    # Print the text summaries
    col2.write("\n歸納總結:\n")
    col2.write(text_summary_mean)
    col2.write(text_summary_median)
    fig = px.box(df_box, x='班級', y='Percentage', points='all', color='班級', width=900)
    st.markdown('### 箱型圖')
    fig.update_traces(boxmean=True)
    st.plotly_chart(fig)


def main():
    if 'subjects' in st.session_state:
        st.write("持續開發中，敬請期待!")
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


def tbd():
    st.write("持續開發中，敬請期待!")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # with open(pkl_file_path, 'rb') as pkl_file:
    #     # Load the data from the Pickle file
    #     a_dic = pickle.load(pkl_file)
    main()
    # st.sidebar.write('版本 V1.1222_2023')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
