import datetime

import pandas as pd
import streamlit as st
from PIL import Image
import streamlit as st
from PIL import Image

from src.utils import data_loader, config


def display_image():
    """Displays an instructional image for file upload format."""
    image = Image.open(config.INSTRUCTION_IMAGE_PATH)
    st.image(image, caption='上傳檔案格式如圖', width=800)


def get_test_date():
    """Prompts the user to input the test date."""
    col1, _ = st.columns(2)
    test_date = col1.date_input("本次考試日期為?", datetime.datetime.today())
    return test_date.isoformat()


def upload_excel_file():
    """Handles the Excel file upload and returns the file path."""
    return st.file_uploader("選擇一個 Excel 文件", type=["xlsx", "xls"])



def process_excel_file(excel_file_path, test_date):
    """
    Processes the uploaded Excel file using the data_loader utility.
    """
    return data_loader.process_excel_file(excel_file_path, test_date)


def main():
    """Main function to handle the Streamlit app workflow."""
    st.title("使用 Streamlit 上傳和處理 Excel 文件")
    display_image()
    test_date = get_test_date()
    excel_file_path = upload_excel_file()

    if excel_file_path is not None:
        with st.spinner('Processing Data...'):
            try:
                data = process_excel_file(excel_file_path, test_date)
                st.session_state.update(data)
                st.success('Excel 檔案已經暫存到記憶體，準備進行下一步分析')
            except ValueError as e:
                st.error(f"資料格式錯誤: {e}")
            except Exception as e:
                st.error(f"發生未預期的錯誤: {e}")


if __name__ == '__main__':
    main()
