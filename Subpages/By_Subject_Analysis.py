# This is a sample Python script.

import plotly_express as px
import streamlit as st

from LocalApps import SharedLayout
from Subpages import Generate_Report


# st.set_page_config(layout="wide")


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Specify the path to your .pkl file
# pkl_file_path = r'../summary.pkl'


def layout_main(a_dic, a_sel, g_m, normal_only):
    if a_sel != "請選擇":

        df = a_dic[a_sel].df.copy()
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
        s_c = s_c.sort_values(by='Percentage', ascending=True)

        # Divide students into 6 groups (R1 to R6)
        if g_m == '一般分法(5組)':
            s_c, a_text, s_p, fig2, a_text2 = Generate_Report.grouping_2(s_c)
        elif g_m == '一般分法(6組)':
            s_c, a_text, s_p, fig2, a_text2 = Generate_Report.grouping_3(s_c)
        else:
            s_c, a_text, s_p, fig2, a_text2 = Generate_Report.grouping_1(s_c)

        # st.dataframe(s_p)
        st.divider()
        st.markdown(a_text)
        col1, col2 = st.columns(2)
        fig = px.bar(s_p, x=s_p.index, y='Percentage', color='Rank')
        fig.update_xaxes(showticklabels=False)
        col1.markdown('Ranking 排列')
        col1.plotly_chart(fig)

        s_minmax = s_p.groupby('Rank')['Percentage'].agg(['min', 'max'])
        s_minmax = s_minmax.reset_index()
        st.markdown('各組答對率 [min max] 值')
        st.dataframe(s_minmax)

        col2.markdown(a_text2)
        col2.plotly_chart(fig2)

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
        fig = SharedLayout.by_class_summary(df, s_c)
        st.plotly_chart(fig)

        st.divider()
        df_sorted = Generate_Report.layout_part_2(df)
        # Group by to get % correct by question and by the whole class year

        st.divider()
        Generate_Report.layout_part_3(df, df_sorted)
        st.success("完成!")


def main():
    if 'subjects' in st.session_state:
        a_dic = st.session_state.subjects
        selections = list(a_dic.keys())
        selections.sort()
        selections.insert(0, "請選擇")
        col1, col2, col3 = st.columns(3)
        a_sel = col1.selectbox("Please select a report", selections)

        g_m = col2.selectbox("選擇分類法", ['一般分法(5組)', '一般分法(6組)', '六等分法'])
        # n_only = col3.toggle('普通班分析')
        n_only = False
        layout_main(a_dic, a_sel, g_m, n_only)
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
