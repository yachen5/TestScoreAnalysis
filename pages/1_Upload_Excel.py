import pandas as pd
import streamlit as st
from PIL import Image
from openpyxl import load_workbook


def main():
    st.title("使用 Streamlit 上傳和處理 Excel 文件")

    # Load your PNG image
    image = Image.open("2023-12-23 013246.png")

    # Display the image using st.image

    st.image(image, caption='上傳檔案格式如圖', width=800)

    # File upload
    excel_file_path = st.file_uploader("選擇一個 Excel 文件", type=["xlsx", "xls"])

    if excel_file_path is not None:
        # Load the Excel workbook
        wb = load_workbook(excel_file_path, read_only=True)

        # Get the names of all worksheets in the Excel file
        worksheet_names = wb.sheetnames

        # Initialize an empty DataFrame to store the combined data
        li = []

        # Loop through each worksheet and append its data to the combined DataFrame
        for sheet_name in worksheet_names:
            # Read data from the current worksheet
            df_t = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=None, engine='openpyxl')
            df_t = df_t.dropna(axis=1)

            # Use the first row as header
            df_t.columns = df_t.iloc[0]

            # Drop the first row (since it's now the header)
            df_t = df_t[1:]
            df_t['年級'] = df_t['班級'].astype(str).str[0]
            df_t['學號'] = 'S' + df_t['學號'].astype(str)

            # Append the data to the combined DataFrame
            li.append(df_t)

        # Close the workbook
        wb.close()

        df = pd.concat(li, ignore_index=True)
        df['年級_科目'] = df['年級'] + '_' + df['科目代號']
        # Split the 'original_column' into individual characters
        df_split = df['答題對錯'].apply(lambda x: pd.Series(list(x)))

        # Rename the columns with the specified naming convention
        df_split.columns = [f'Q_{str(n).zfill(2)}' for n in range(1, len(df_split.columns) + 1)]

        # Concatenate the split columns with the original DataFrame
        df = pd.concat([df, df_split], axis=1)

        # Drop the original column
        df = df.drop(columns=['答題對錯'])
        # Extract columns starting with 'Q' as value_vars
        value_vars = [col for col in df.columns if col.startswith('Q')]

        # Melt the DataFrame
        melted_df = pd.melt(df, id_vars=[col for col in df.columns if col not in value_vars],
                            value_vars=value_vars, var_name='Question', value_name='Answer')
        melted_df = melted_df.drop('答題狀況', axis=1)
        # Find unique values in column 'AA'
        unique_values = melted_df['年級_科目'].unique()

        # Create a dictionary with 'AA' values as keys and filtered DataFrames as values
        result_dict = {}

        for value in unique_values:
            filtered_df = melted_df[melted_df['年級_科目'] == value].copy()
            st.write(f'Processing {value}')
            result_dict[value] = filtered_df

        st.session_state.groups = result_dict
        st.success('Excel file loaded into memory and ready to be analyzed')


if __name__ == '__main__':
    main()
