import pandas as pd
import plotly_express as px
import streamlit as st

from LocalApps.SharedObjects import get_excel_download, convert_stats


def by_class_summary(df, s_c):
    """
    Generate a summary of class performance and rankings.

    Args:
        df (DataFrame): The input DataFrame containing student performance data.
        s_c (DataFrame): The input DataFrame containing student information.

    Returns:
        fig (Figure): The generated box plot figure.

    """
    st.markdown('### 各班成績分布與排名')
    col1, col2 = st.columns(2)
    # st.dataframe(df)
    df_box = df.groupby(['班級', '學號'], as_index=False).agg({'Question': 'count'})
    df_box = df_box.merge(s_c, on=['學號'], how='left')
    df_desc = df_box.groupby(['班級'])['Percentage'].describe()
    df_desc2 = convert_stats(df_desc)

    col1.dataframe(df_desc2)
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
    fig = px.box(df_box, x='班級', y='Percentage', points='all', color='班級')
    st.markdown('### 箱型圖')
    fig.update_traces(boxmean=True)
    return fig
    # st.plotly_chart(fig)


def layout_class(include_all=False):
    """
    Renders the layout for analyzing class performance.

    Args:
        include_all (bool, optional): Whether to include all subjects or select specific subjects. Defaults to False.

    Returns:
        None
    """
    a_dic = st.session_state.class_groups
    # col1, col2 = st.columns(2)
    selections = list(a_dic.keys())
    selections.sort()
    selections.insert(0, "請選擇")
    a_selection = st.selectbox("請選擇一個班級", selections)
    # st.write(a_selection)
    if a_selection != "請選擇":
        subjects = st.session_state['subjects']
        a_class = a_dic[a_selection]
        # st.write(a_class.class_numbers)
        # st.dataframe(a_class.students)
        li_ek = []
        if include_all:
            subject_list = a_class.subjects
        else:
            subject_list = st.multiselect("請選擇科目 (可複選)", a_class.subjects)
        # col_list = [col1, col2]
        count = 0
        for a_subject in subject_list:
            subject_class = subjects[a_subject]
            df = subject_class.idv_score.copy()
            # df['Percentage'] = round(df['Percentage'] * 100, )
            df['Groups'] = df['學號'].apply(lambda x: a_selection if x in a_class.student_numbers else '其他班')
            df = df.sort_values(by=['Groups'])
            st.dataframe(df)
            st.subheader(f"{a_subject} 本班與其他班的箱型圖比較")
            st.markdown('可參考 中位數與高低分差')
            fig = px.box(df, x='Groups', y='Percentage', facet_col='Groups', color='Groups')
            fig.update_traces(boxmean=True)
            st.plotly_chart(fig)
            df_desc = df.groupby(['Groups'])['Percentage'].describe()
            df_desc = convert_stats(df_desc)
            st.markdown('統計表')
            st.dataframe(df_desc)

            q_correct = subject_class.correct_rate(a_class.student_numbers, True)
            q_correct['Group'] = '其他班'
            q_correct2 = subject_class.correct_rate(a_class.student_numbers, False)
            q_correct2['Group'] = a_selection

            df_merge = q_correct.merge(q_correct2, on=['Question'], how='left')
            # st.dataframe(df_merge)
            st.write("""
            柱狀圖示本班各題的答對率
            
            Delta是本班答對率 減掉 其他班答對率  >0:本班較佳 <0:其他班較佳
            
            顏色越紅，該題建議重點複習!
            """)
            df_merge['Delta'] = df_merge['Percentage_y'] - df_merge['Percentage_x']
            df_merge = df_merge[['Question', 'Delta']]
            q_correct2 = q_correct2.merge(df_merge, on='Question', how='left')
            # st.dataframe(df_merge)
            # q_c_all = pd.concat([q_correct, q_correct2], ignore_index=True)
            fig = px.bar(q_correct2, x='Question', y='Percentage', text='percentage_text', color='Delta',
                         color_continuous_scale=[(0, "red"), (0.5, "lightgray"), (1, "green")],
                         color_continuous_midpoint=0)

            # fig.add_trace(px.line(df_merge, x='Question', y='Delta', color_discrete_sequence=['red']).data[0])
            st.plotly_chart(fig)
            df_ek = subject_class.error_rank.copy()
            df_ek = df_ek[df_ek['學號'].isin(a_class.student_numbers)]
            df_small = df[['學號', 'PG']].copy()
            df_ek = df_ek.merge(df_small, on=['學號'], how='left')
            # st.dataframe(df_ek)
            li_ek.append(df_ek)
            count += 1
            st.divider()

        if len(subject_list) > 0:
            st.markdown("""
            分析各學生回答錯誤的題目，對應到全年級的答對率
            
            全年級答對率越高，該學生的該題要加強複習
            
            答對率低於基準線以下的題目不列入分析""")
            # col1, col2 = st.columns(2)
            selected_min = st.number_input('請選擇全年級答對率的基準線', min_value=0.5, max_value=1.0, value=0.7,
                                           step=0.1)

            df_ek_all = pd.concat(li_ek, ignore_index=True)
            df_ek_all = df_ek_all.dropna(subset=['Percentage'])
            df_ek_sub = df_ek_all[df_ek_all['Percentage'] >= selected_min]
            df_ek_sub = df_ek_sub.sort_values(by=['學號', '科目代號', 'Percentage'], ascending=[True, True, False])
            # df_ek_sub = df_ek_sub[df_ek_sub['學號'].isin(a_class.class_numbers)]
            if include_all:
                pass
            else:
                pick_student = st.selectbox("請選擇一個學號", a_class.student_numbers)
                df_ek_sub = df_ek_sub[df_ek_sub['學號'] == pick_student]

            df_ek_sub = df_ek_sub[
                ['班級', '座號', '學號', '科目代號', 'Question', 'Answer', 'Percentage', 'percentage_text', 'PG']]
            # df_ek_all = df_ek_all.sort_values(by=['學號'])
            st.dataframe(df_ek_sub)
            get_excel_download(df_ek_sub)

        # st.dataframe(q_correct)
