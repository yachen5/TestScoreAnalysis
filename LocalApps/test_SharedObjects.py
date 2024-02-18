import pandas as pd

from SharedObjects import calculate_percentage

# Test case 1: Empty DataFrame
df_empty = pd.DataFrame(columns=['A', 'B', 'C', 'D'])
group_cols = ['A', 'B']
by_col = 'C'
sum_col = 'D'
expected_output_empty = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'Percentage', 'percentage_text'])
assert calculate_percentage(df_empty, group_cols, by_col, sum_col).equals(expected_output_empty)

# Test case 2: Single group, single row
df_single_row = pd.DataFrame({'A': ['Group1'], 'B': ['Subgroup1'], 'C': ['Category1'], 'D': [10]})
group_cols = ['A', 'B']
by_col = 'C'
sum_col = 'D'
expected_output_single_row = pd.DataFrame(
    {'A': ['Group1'], 'B': ['Subgroup1'], 'C': ['Category1'], 'D': [10], 'Percentage': [1.0],
     'percentage_text': ['100%']})
assert calculate_percentage(df_single_row, group_cols, by_col, sum_col).equals(expected_output_single_row)

# Test case 3: Multiple groups, multiple rows
df_multiple_rows = pd.DataFrame(
    {'A': ['Group1', 'Group1', 'Group2', 'Group2'], 'B': ['Subgroup1', 'Subgroup2', 'Subgroup1', 'Subgroup2'],
     'C': ['Category1', 'Category1', 'Category2', 'Category2'], 'D': [10, 20, 30, 40]})
group_cols = ['A', 'B']
by_col = 'C'
sum_col = 'D'
expected_output_multiple_rows = pd.DataFrame(
    {'A': ['Group1', 'Group1', 'Group2', 'Group2'], 'B': ['Subgroup1', 'Subgroup2', 'Subgroup1', 'Subgroup2'],
     'C': ['Category1', 'Category1', 'Category2', 'Category2'], 'D': [10, 20, 30, 40],
     'Percentage': [0.333333, 0.666667, 0.428571, 0.571429], 'percentage_text': ['33%', '66%', '42%', '57%']})
assert calculate_percentage(df_multiple_rows, group_cols, by_col, sum_col).equals(expected_output_multiple_rows)

# Test case 4: No group columns
df_no_group_cols = pd.DataFrame(
    {'A': ['Group1', 'Group1', 'Group2', 'Group2'], 'B': ['Subgroup1', 'Subgroup2', 'Subgroup1', 'Subgroup2'],
     'C': ['Category1', 'Category1', 'Category2', 'Category2'], 'D': [10, 20, 30, 40]})
group_cols = []
by_col = 'C'
sum_col = 'D'
expected_output_no_group_cols = pd.DataFrame(
    {'A': ['Group1', 'Group1', 'Group2', 'Group2'], 'B': ['Subgroup1', 'Subgroup2', 'Subgroup1', 'Subgroup2'],
     'C': ['Category1', 'Category1', 'Category2', 'Category2'], 'D': [10, 20, 30, 40],
     'Percentage': [0.25, 0.25, 0.25, 0.25], 'percentage_text': ['25%', '25%', '25%', '25%']})
assert calculate_percentage(df_no_group_cols, group_cols, by_col, sum_col).equals(expected_output_no_group_cols)

print("All test cases passed!")
