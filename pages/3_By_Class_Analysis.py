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
    if a_selection != "請選擇":
        subjects = st.session_state['subjects']
        a_class = a_dic[a_selection]
        # st.write(a_class.class_numbers)
        # st.dataframe(a_class.students)
        subject_list = col2.multiselect("請選擇科目", a_class.subjects)
        col_list = [col1, col2]
        count = 0
        for a_subject in subject_list:
            a_col = col_list[count % 2]
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
            count += 1


if __name__ == '__main__':
    # with open(pkl_file_path, 'rb') as pkl_file:
    #     # Load the data from the Pickle file
    #     a_dic = pickle.load(pkl_file)
    if 'class_groups' in st.session_state:
        layout_main()


    else:
        st.warning("請回到前一步驟，上傳Excel文件")
    # st.sidebar.write('版本 V1.1222_2023')
