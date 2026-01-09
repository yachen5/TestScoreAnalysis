# This is a sample Python script.

import plotly_express as px
import streamlit as st

from LocalApps import SharedLayout
from Subpages import Generate_Report
from src.analysis.analyzer import AssessmentAnalyzer


# st.set_page_config(layout="wide")


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Specify the path to your .pkl file
# pkl_file_path = r'../summary.pkl'


def layout_main(a_dic, a_sel, g_m, normal_only):
    if a_sel != "請選擇":
        subject_data = a_dic[a_sel]
        analyzer = AssessmentAnalyzer(subject_data)
        
        # Basic Info Display
        df = subject_data.df.copy()
        class_year = df['年級'].iloc[0]
        subj = df['科目代號'].iloc[0]
        st.markdown(f"## {class_year}年級 {subj}科分析")

        # Perform Analysis
        results = analyzer.perform_grouping_analysis(method=g_m, normal_only=normal_only)
        s_c = results['student_data']
        df_merged = results['full_df_with_rank']
        
        # Visualization Logic (kept in UI layer for now, but using cleaner data)
        st.divider()
        st.markdown(results['summary_text_1'])
        col1, col2 = st.columns(2)
        
        # Plot 1: Ranking
        # Prepare data for plotting
        if 'R1' in str(s_c['Rank'].iloc[0]): # Check if it is R-grouping (Quantile)
             s_p = s_c.reset_index(drop=True)
             fig = px.bar(s_p, x=s_p.index, y='Percentage', color='Rank')
        else: # Score grouping
             s_count = s_c.groupby('Rank').agg({'學號': 'count'}).reset_index()
             fig = px.bar(s_count, x='Rank', y='學號', text='學號', color='Rank')

        fig.update_xaxes(showticklabels=False)
        col1.markdown('Ranking 排列')
        col1.plotly_chart(fig)

        # Plot 2: Slope or Count
        col2.markdown(results['summary_text_2'])
        if 'R1' in str(s_c['Rank'].iloc[0]):
             s_avg = s_c.groupby('Rank').agg({'Percentage': 'mean'}).reset_index()
             s_avg['percentage_text'] = s_avg['Percentage'].apply(lambda x: f'{int(x * 100)}%')
             fig2 = px.line(s_avg, x='Rank', y='Percentage', text='percentage_text')
             fig2.update_traces(textposition='top center')
             fig2.update_layout(yaxis=dict(range=[0, max(s_avg['Percentage'] + 0.2)]))
             col2.plotly_chart(fig2)
             
             # Min Max Table
             s_minmax = s_c.groupby('Rank')['Percentage'].agg(['min', 'max']).reset_index()
             st.markdown('各組答對率 [min max] 值')
             st.dataframe(s_minmax)
        else:
             # For score grouping, maybe just show the table or same distribution?
             # Original code for grouping_2/3 showed similar bar chart or count.
             # We already showed count in fig 1 for this mode.
             pass

        st.divider()
        fig = SharedLayout.by_class_summary(df_merged, s_c)
        st.plotly_chart(fig)

        st.divider()
        # Continuing to use Generate_Report for part 2 and 3 for now as they are complex
        # Ideally should be refactored later
        df_sorted = Generate_Report.layout_part_2(df_merged)
        st.divider()
        Generate_Report.layout_part_3(df_merged, df_sorted)
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
