
import io
import streamlit as st

def get_excel_download(df):
    excel_file = io.BytesIO()
    df.to_excel(excel_file, index=False)  # Adjust parameters as needed
    # Create a download button with appropriate label and mimetype
    st.download_button(
        label="下載上列的Excel報表",
        data=excel_file.getvalue(),
        file_name="data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
