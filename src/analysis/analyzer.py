from typing import Dict, Any, Tuple, List, Optional
from src.models.subject import Subject
from src.analysis import statistics
import pandas as pd
import plotly_express as px

class AssessmentAnalyzer:
    """
    Analyzer for assessment data. Decouples analysis logic from data models.
    """

    def __init__(self, subject_data: Subject):
        self.subject: Subject = subject_data



    def perform_grouping_analysis(self, method='5_groups', normal_only=False):
        """
        Performs grouping analysis on the subject data.
        
        Args:
           method: The grouping method to use ('5_groups', '6_groups', etc.)
           normal_only: Whether to filter only normal students.
           
        Returns:
            dict: Contains sorted_df, plot_data
        """
        df = self.subject.df.copy()
        
        # Logic for normal/special filtering (previously in layout_main)
        class_year = df['年級'].iloc[0]
        unique_values = sorted(df['班級'].unique())
        last_unique_value = unique_values[-1] if unique_values else None
        
        df['label'] = 'normal'
        if last_unique_value:
             df.loc[df['班級'] == last_unique_value, 'label'] = 'special'
             
        if normal_only:
            df = df[df['label'] == 'normal']
            
        # Group by to get % correct by student
        # s_df = df.groupby(['學號', 'Answer']).agg({'Question': 'count'})
        # s_df['Percentage'] = s_df.groupby(['學號'])['Question'].transform(lambda x: x / x.sum())
        s_df = statistics.calculate_percentage(df, ['學號'], 'Answer', 'Question')
        
        s_c = s_df[s_df['Answer'] == '.'].copy()
        s_c = s_c.sort_values(by='Percentage', ascending=True)

        # Grouping Logic
        if method == '一般分法(5組)':
             bins = [0, 0.6, 0.7, 0.8, 0.9, 1.1]
             labels = ['<60', '60-69', '70-79', '80-89', '>90']
             s_c, r_text, r_text2 = self._ten_group_students(s_c, bins, labels)
        elif method == '一般分法(6組)':
             bins = [0, 0.3, 0.6, 0.7, 0.8, 0.9, 1.1]
             labels = ['<30', '30-59', '60-69', '70-79', '80-89', '>90']
             s_c, r_text, r_text2 = self._ten_group_students(s_c, bins, labels)
        else:
             # Default 6-part split (R1-R6)
             s_c, r_text, r_text2 = self._group_by_quantile(s_c, 6)

        return {
            'student_data': s_c,
            'summary_text_1': r_text,
            'summary_text_2': r_text2,
            'full_df_with_rank': df.merge(s_c[['學號', 'Rank']], on=['學號'], how='left')
        }

    def _ten_group_students(self, s_c, bins, labels):
        s_c = s_c.copy()
        s_c['Rank'] = pd.cut(s_c['Percentage'], bins=bins, labels=labels, right=False)
        r_text = f"""### Ranking (Custom Groups)
        - 先把全年級學生當科答對率(1=100%)，從最低排到最高
        - 每根bar代表一位學生，移除學號
        - 分成 {len(labels)} 群"""
        r_text2 = "各組人數"
        return s_c, r_text, r_text2
        
    def _group_by_quantile(self, s_c, num_groups):
        s_c = s_c.copy()
        group_size = len(s_c) // num_groups
        # Safe guard for empty or small groups
        if group_size == 0:
             s_c['Rank'] = 'R1'
        else:
            bins = [-1] + [i * group_size for i in range(1, num_groups)] + [len(s_c)]
            # Fix if bins are not unique? pd.cut handles unique logic if needed but mostly here indexes are unique
            labels = [f'R{i}' for i in range(1, num_groups + 1)]
            s_c['Rank'] = pd.cut(pd.RangeIndex(len(s_c)), bins=bins, labels=labels, include_lowest=True)
            
        r_text = f"""### R1~R{num_groups} 分群曲線
        - 先把全年級學生當科答對率(1=100%)，從最低排到最高
        - 每根bar代表一位學生，移除學號
        - 分成 {num_groups} 等分: R1是最高分的一組，到R{num_groups}是最低分的一組"""
        r_text2 = "各組平均答對率 斜率圖(各組變化太大須注意)"
        return s_c, r_text, r_text2

