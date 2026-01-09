import numpy as np
import pandas as pd

def calculate_percentage(df, group_cols, by_col, sum_col):
    """Calculate the percentage of a column's sum within groups.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        group_cols (list): The columns to group by.
        by_col (str): The column to calculate the percentage by.
        sum_col (str): The column to sum within groups.

    Returns:
        pandas.DataFrame: The DataFrame with the calculated percentage column.
    """
    df = df.copy()
    if not group_cols:
        grouped = df.groupby([by_col]).agg({sum_col: 'count'})
    else:
        grouped = df.groupby(group_cols + [by_col]).agg({sum_col: 'count'})
    
    # Needs to merge back/transform to keep shape if that was the intent, 
    # but the original code used transform on the grouped object to assign back to original df?
    # Let's look at original logic:
    # df.groupby(group_cols + [by_col]).agg({sum_col: 'count'}) -> This reduces rows.
    # original: df.groupby(group_cols)[sum_col].transform(lambda x: x / x.sum())
    
    # Re-implementing strictly as per original logic but cleaning it up
    # The original function mixed aggregation and transformation which is tricky.
    # It returned a dataframe with 'Percentage' and 'percentage_text' and 'Question', 'Answer' etc columns?
    # Original function:
    # df = df.groupby(group_cols + [by_col]).agg({sum_col: 'count'})  <-- This reduces it to unique combinations
    # if len(group_cols) == 0: ...
    # else: df['Percentage'] = df.groupby(group_cols)[sum_col].transform(lambda x: x / x.sum())
    
    df_agg = df.groupby(group_cols + [by_col]).agg({sum_col: 'count'})
    
    if len(group_cols) == 0:
        df_agg['Percentage'] = df_agg[sum_col] / df_agg[sum_col].sum()
    else:
        # Group by the group_cols ONLY to get the denominator
        # The df_agg has index (group_cols + by_col)
        # We need to groupby the level(s) of group_cols
        level_indices = list(range(len(group_cols)))
        df_agg['Percentage'] = df_agg.groupby(level=level_indices)[sum_col].transform(lambda x: x / x.sum())

    df_agg['Percentage'] = df_agg['Percentage'].fillna(0)
    df_agg = df_agg.reset_index()
    df_agg['percentage_text'] = df_agg['Percentage'].apply(lambda x: f'{int(x * 100)}%')
    return df_agg

def assign_ten_groups(df):
    """Assigns students to 10 groups based on their scores."""
    group_size = len(df) // 10
    if group_size == 0: # Handle small datasets
        df['PW'] = 1
        return df
        
    df = df.sort_values('Percentage', ascending=True)
    # Provide labels and bins. Note: original code hardcoded specific logic.
    # We'll use pd.qcut if possible, but adhering to original logic for consistency first.
    # Original used pd.cut with explicit bins based on count.
    
    bins = [-1] + [i * group_size for i in range(1, 10)] + [len(df)]
    # Ensure bins are unique (though with count based, they should be strictly increasing unless group_size is 0)
    # The original logic used np.arange(len(df)) as the value to cut.
    
    df['PW'] = pd.cut(np.arange(len(df)),
                      bins=bins,
                      labels=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
                      include_lowest=True, ordered=False) # ordered=False to allow numeric type if possible or just labels
    return df.copy()

def assign_four_groups(df):
    """Assigns students to 4 groups (PL, PML, PMH, PH)."""
    group_size = len(df) // 4
    if group_size == 0:
        df['PG'] = 'PH'
        return df
        
    df = df.sort_values('Percentage', ascending=True)
    bins = [-1, group_size, 2 * group_size, 3 * group_size, len(df)]
    
    df['PG'] = pd.cut(np.arange(len(df)),
                      bins=bins,
                      labels=['PL', 'PML', 'PMH', 'PH'], 
                      include_lowest=True)
    return df.copy()

def top_error_questions(group):
    return group.nlargest(5, 'Percentage')

def convert_stats(df_desc):
    """Converts statistical summary dataframe to a more readable format."""
    df_desc2 = df_desc.rename(
        columns={'count': '人數', 'mean': '平均', 'std': '標準差', 'min': '最低分', '25%': '25%', '50%': '中位數',
                 '75%': '75%', 'max': '最高分'})
    # convert dicimals to percentage for better readability
    cols_to_convert = ['平均', '標準差', '最低分', '25%', '中位數', '75%', '最高分']
    # Convert columns to percentage
    for col in cols_to_convert:
        if col in df_desc2.columns:
            df_desc2[col] = round(df_desc2[col] * 100, 2)
    return df_desc2
    return df_desc2

def dis_index(df):
    """
    Calculate the percentage of students with a specific answer in each performance group.

    :param df: DataFrame containing student data.
    :return: Tuple of two floats representing the percentage of students with '.' answer in 'PH' and 'PL' performance groups.
    """
    df = assign_four_groups(df)
    # st.dataframe(df)
    df_g = df.groupby(['PG', 'Answer']).agg({'學號': 'count'})
    df_g['Percentage'] = df_g.groupby(['PG'])['學號'].transform(lambda x: x / x.sum())
    df_g = df_g.reset_index()
    df_p = df_g[df_g['Answer'] == '.']
    df_p = df_p.set_index('PG')
    
    # Safe access
    ph = round(df_p.loc['PH', 'Percentage'], 3) if 'PH' in df_p.index else 0
    pl = round(df_p.loc['PL', 'Percentage'], 3) if 'PL' in df_p.index else 0
    
    return ph, pl
