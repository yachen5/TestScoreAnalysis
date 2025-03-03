"""Utility functions for data processing and analysis."""
from typing import List, Tuple, Union, Optional
import pandas as pd
import numpy as np
from typing import Dict


def calculate_percentage(df: pd.DataFrame,
                       group_cols: List[str],
                       by_col: str,
                       sum_col: str) -> pd.DataFrame:
    """Calculate the percentage of a column's sum within groups.

    Args:
        df: The input DataFrame.
        group_cols: The columns to group by.
        by_col: The column to calculate the percentage by.
        sum_col: The column to sum within groups.

    Returns:
        DataFrame with calculated percentage and percentage_text columns.
    """
    df = df.copy()
    df = df.groupby(group_cols + [by_col]).agg({sum_col: 'count'})
    if len(group_cols) == 0:
        df['Percentage'] = df[sum_col].transform(lambda x: x / len(df))
    else:
        df['Percentage'] = df.groupby(group_cols)[sum_col].transform(lambda x: x / x.sum())
    df['Percentage'] = df['Percentage'].fillna(0)
    df = df.reset_index()
    df['percentage_text'] = df['Percentage'].apply(lambda x: f'{int(x * 100)}%')
    return df


def assign_groups(df: pd.DataFrame,
                 score_column: str,
                 num_groups: int,
                 group_labels: List[Union[str, float]],
                 output_column: str) -> pd.DataFrame:
    """Assign students to groups based on their scores.

    Args:
        df: DataFrame containing student data
        score_column: Column name containing scores
        num_groups: Number of groups to divide into
        group_labels: Labels for each group
        output_column: Name of the output column for group assignments

    Returns:
        DataFrame with new group assignment column
    """
    df = df.copy()
    group_size = len(df) // num_groups
    df = df.sort_values(score_column, ascending=True)
    
    bins = [-1] + [i * group_size for i in range(1, num_groups)] + [len(df)]
    df[output_column] = pd.cut(np.arange(len(df)),
                              bins=bins,
                              labels=group_labels,
                              include_lowest=True)
    return df


def assign_ten_groups(df: pd.DataFrame) -> pd.DataFrame:
    """Assign students to 10 performance groups (0.1 to 1.0).

    Args:
        df: DataFrame containing student data with 'Percentage' column

    Returns:
        DataFrame with new 'PW' column containing group assignments
    """
    return assign_groups(
        df=df,
        score_column='Percentage',
        num_groups=10,
        group_labels=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        output_column='PW'
    )


def assign_four_groups(df: pd.DataFrame) -> pd.DataFrame:
    """Assign students to 4 performance groups (PL, PML, PMH, PH).

    Args:
        df: DataFrame containing student data with 'Percentage' column

    Returns:
        DataFrame with new 'PG' column containing group assignments
    """
    return assign_groups(
        df=df,
        score_column='Percentage',
        num_groups=4,
        group_labels=['PL', 'PML', 'PMH', 'PH'],
        output_column='PG'
    )


def top_error_questions(group: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Find the top N error questions from a group.

    Args:
        group: DataFrame containing question data
        n: Number of top errors to return (default: 5)

    Returns:
        DataFrame containing the top N error questions
    """
    return group.nlargest(n, 'Percentage')


def convert_stats(df_desc: pd.DataFrame) -> pd.DataFrame:
    """Convert statistical summary DataFrame to a more readable format.

    Args:
        df_desc: Statistical summary DataFrame

    Returns:
        DataFrame with renamed columns and converted percentage values
    """
    column_mapping = {
        'count': '人數',
        'mean': '平均',
        'std': '標準差',
        'min': '最低分',
        '25%': '25%',
        '50%': '中位數',
        '75%': '75%',
        'max': '最高分'
    }
    
    df_desc2 = df_desc.rename(columns=column_mapping)
    
    # Convert decimals to percentages
    percentage_columns = ['平均', '標準差', '最低分', '25%', '中位數', '75%', '最高分']
    for col in percentage_columns:
        if col in df_desc2.columns:
            df_desc2[col] = round(df_desc2[col] * 100, 2)
            
    return df_desc2


def calculate_distinguish_rate(df: pd.DataFrame,
                             group_column: str = 'PG',
                             correct_answer: str = '.') -> Tuple[float, float]:
    """Calculate the distinguish rate between high and low performing groups.

    Args:
        df: DataFrame containing student performance data
        group_column: Column name for performance groups
        correct_answer: Symbol representing correct answers

    Returns:
        Tuple of (high_group_rate, low_group_rate)
    """
    df = assign_four_groups(df)
    df_g = df.groupby([group_column, 'Answer']).agg({'學號': 'count'})
    df_g['Percentage'] = df_g.groupby([group_column])['學號'].transform(lambda x: x / x.sum())
    df_g = df_g.reset_index()
    
    df_p = df_g[df_g['Answer'] == correct_answer]
    df_p = df_p.set_index(group_column)
    
    ph = round(df_p.loc['PH', 'Percentage'], 3)
    pl = round(df_p.loc['PL', 'Percentage'], 3)
    
    return ph, pl 