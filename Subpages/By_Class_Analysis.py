import pandas as pd
import plotly_express as px
import streamlit as st

st.markdown("""
            持續開發中，敬請期待!""")


def layout_main():
    a_dic = st.session_state.class_groups
    col1, col2 = st.columns(2)
    selections = list(a_dic.keys())
    selections.sort()
    selections.insert(0, "請選擇")
    a_selection = col1.selectbox("請選擇一個班級", selections)
    # st.write(a_selection)
    if (a_selection != "請選擇"):
        subjects = st.session_state['subjects']
        a_class = a_dic[a_selection]
        # st.write(a_class.class_numbers)
        # st.dataframe(a_class.students)
        li_ek = []
        subject_list = col2.multiselect("請選擇科目 (可複選)", a_class.subjects)
        col_list = [col1, col2]
        count = 0
        for a_subject in subject_list:
            a_col = col_list[count % 1]
            subject_class = subjects[a_subject]
            df = subject_class.idv_score.copy()
            df['Percentage'] = round(df['Percentage'] * 100, )
            df['Groups'] = df['學號'].apply(lambda x: a_selection if x in a_class.class_numbers else '其他班')
            df = df.sort_values(by=['Groups'])
            # st.dataframe(df)
            a_col.subheader(f"{a_subject} 本班與其他班的箱型圖比較")
            a_col.markdown('可參考 中位數與高低分差')
            fig = px.box(df, x='Groups', y='Percentage', facet_col='Groups', color='Groups')
            a_col.plotly_chart(fig)
            df_desc = df.groupby(['Groups'])['Percentage'].describe()
            a_col.markdown('統計表')
            a_col.dataframe(df_desc)

            q_correct = subject_class.correct_rate(a_class.class_numbers, True)
            q_correct['Group'] = '其他班'
            q_correct2 = subject_class.correct_rate(a_class.class_numbers, False)
            q_correct2['Group'] = a_selection

            df_merge = q_correct.merge(q_correct2, on=['Question'], how='left')
            # a_col.dataframe(df_merge)
            a_col.write("""
            柱狀圖示本班各題的答對率
            
            Delta是本班答對率 減掉 其他班答對率  >0:本班較佳 <0:其他班較佳
            
            顏色越紅，該題建議重點複習!
            """)
            df_merge['Delta'] = df_merge['Percentage_y'] - df_merge['Percentage_x']
            df_merge = df_merge[['Question', 'Delta']]
            q_correct2 = q_correct2.merge(df_merge, on='Question', how='left')
            # a_col.dataframe(df_merge)
            # q_c_all = pd.concat([q_correct, q_correct2], ignore_index=True)
            fig = px.bar(q_correct2, x='Question', y='Percentage', text='percentage_text', color='Delta',
                         color_continuous_scale=[(0, "red"), (0.5, "lightgray"), (1, "green")],
                         color_continuous_midpoint=0)

            # fig.add_trace(px.line(df_merge, x='Question', y='Delta', color_discrete_sequence=['red']).data[0])
            a_col.plotly_chart(fig)
            df_ek = subject_class.error_rank.copy()
            li_ek.append(df_ek)
            count += 1
            a_col.divider()

        if len(subject_list) > 0:
            st.markdown("""
            分析各學生回答錯誤的題目，對應到全年級的答對率
            
            全年級答對率越高，該學生的該題要加強複習
            
            答對率低於基準線以下的題目不列入分析""")
            col1, col2 = st.columns(2)
            a_student = col1.selectbox("請選擇一個學號", a_class.class_numbers)

            df_ek_all = pd.concat(li_ek, ignore_index=True)
            df_ek_all = df_ek_all.dropna(subset=['Percentage'])
            df_ek_all = df_ek_all[df_ek_all['學號'] == a_student]
            df_ek_all = df_ek_all.sort_values(by=['科目代號', 'Percentage'], ascending=False)

            selected_min = col2.number_input('請選擇全年級答對率的基準線', min_value=0.5, max_value=1.0, value=0.6,
                                             step=0.1)
            df_ek_all = df_ek_all[df_ek_all['Percentage'] >= selected_min]
            df_ek_all = df_ek_all[
                ['班級', '座號', '學號', '科目代號', 'Question', 'Answer', 'Percentage', 'percentage_text']]
            # df_ek_all = df_ek_all.sort_values(by=['學號'])
            st.dataframe(df_ek_all)

        # st.dataframe(q_correct)


def main():
    # with open(pkl_file_path, 'rb') as pkl_file:
    #     # Load the data from the Pickle file
    #     a_dic = pickle.load(pkl_file)
    if 'class_groups' in st.session_state:
        layout_main()

    else:
        st.warning("請回到前一步驟，上傳Excel文件")


if __name__ == '__main__':
    main()
    # st.sidebar.write('版本 V1.1222_2023')
