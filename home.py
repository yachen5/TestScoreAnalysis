# This is a sample Python script.
import numpy as np
import pandas as pd
import plotly_express as px
import streamlit as st

st.set_page_config(layout="wide")

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pickle

# Specify the path to your .pkl file
pkl_file_path = r'C:\Users\admin\Documents\Python Scripts\HK Analysis\summary.pkl'


def layout_main(a_dic, a_sel):
    if a_sel is not None:
        df = a_dic[a_sel]
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
        # st.dataframe(s_c)
        fig = px.bar(s_c, x='學號', y='Percentage', color='Rank', width=1200, height=600)
        fig.update_xaxes(showticklabels=False)
        st.plotly_chart(fig)
        b_len = len(df)
        df = df.merge(s_c, on=['學號'], how='left')
        a_len = len(df)

        # to make sure total rows does not increase after merge
        if a_len != b_len:
            st.error('Please check ranking calculation! Unique student id as output')
            st.stop()
        # st.dataframe(df)

        # Group by to get % correct by question and by the whole class year
        grouped_df = df.groupby(['年級', 'Question', 'Answer']).agg({'學號': 'count'})
        grouped_df['Percentage'] = grouped_df.groupby(['年級', 'Question'])['學號'].transform(lambda x: x / x.sum())
        grouped_df = grouped_df.reset_index()
        grouped_df['percentage_text'] = grouped_df['Percentage'].apply(lambda x: f'{int(x * 100)}%')
        df_1 = grouped_df.copy()

        fig = px.bar(df_1, x='Question', y='Percentage', color='Answer', text='percentage_text', facet_row='年級',
                     width=1200, height=600)
        st.markdown('### Standard Report')
        st.plotly_chart(fig)
        df_a = df_1[df_1['Answer'] == '.'].copy()
        df_a = df_a.drop(['學號', 'Answer'], axis=1)

        df_sorted = df_a.sort_values(by='Percentage')

        fig = px.bar(df_sorted, x='Question', y='Percentage', text='percentage_text', color='Percentage', width=1200,
                     height=600, color_continuous_scale=["red", "green"])
        st.markdown('### Sorted by 答對率')
        st.plotly_chart(fig)

        st.markdown("### 單一問題分析")
        col1, col2, col3 = st.columns(3)
        # Add form components
        qs = list(df_sorted['Question'].unique())
        # qs.sort()
        a_q = col1.selectbox('請選擇一個題目', qs)
        op = [None, '全年級', '分班']
        a_p = col2.selectbox('分析方法', op)
        if a_p == '分班':
            cc = list(df['班級'].unique())
            cc.sort()
            # cc.insert(0, 'All')
            a_c = col3.selectbox('選擇班級', cc)
            # submitted = st.form_submit_button("Submit")

        # Display the entered values after form submission
        if a_p is not None:
            if a_p == '分班':
                # cc = list(df['班級'].unique())
                # cc.sort()
                # # cc.insert(0, 'All')
                # a_c = st.selectbox('選擇班級', cc)
                df_q = df[(df['Question'] == a_q) & (df['班級'] == a_c)]
                st.dataframe(df_q)
            else:
                grouped_df = df.groupby(['年級', '班級', 'Question', 'Answer']).agg({'學號': 'count'})
                grouped_df['Percentage'] = grouped_df.groupby(['年級', '班級', 'Question'])['學號'].transform(
                    lambda x: x / x.sum())
                grouped_df = grouped_df.reset_index()
                grouped_df['percentage_text'] = grouped_df['Percentage'].apply(lambda x: f'{int(x * 100)}%')
                # Display the grouped DataFrame with counts
                st.dataframe(grouped_df)

            # st.success(f"Name: {name}, Age: {age}, Email: {email}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open(pkl_file_path, 'rb') as pkl_file:
        # Load the data from the Pickle file
        a_dic = pickle.load(pkl_file)

    selections = list(a_dic.keys())
    selections.sort()
    selections.insert(0, None)
    a_sel = st.sidebar.selectbox("Please select a report", selections)
    layout_main(a_dic, a_sel)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
