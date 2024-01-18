import streamlit as st

from st_pages import Page, show_pages

# Optional -- adds the title and icon to the current page
# add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("home.py", "Home", ":school:"),
        Page("pages/1_Upload_Excel.py", "上傳Excel檔案", ":green_book:"),
        Page("pages/2_Generate_Reports.py", "科任老師報表與分析", ":bar_chart:"),
        Page("pages/3_By_Class_Analysis.py", "導師專區(建構中)", ":triangular_ruler:"),
    ]
)

st.markdown("""
**(以下文字由ChatGPT提供)**

歡迎使用我們的網站！

我們提供一個簡單而強大的平台，讓您能夠輕鬆上傳測驗結果的 Excel 檔案，並進行詳細的分析。這個網站設計得易於使用，讓您能夠快速上手，進而深入瞭解您的測驗數據。

主要功能包括：

- 上傳檔案： 您可以使用我們的檔案上傳功能，輕鬆選擇並上傳測驗結果的 Excel 檔案。
- 數據分析： 我們使用強大的 Pandas 庫進行數據處理，以便您能夠執行各種詳細的分析，從而瞭解測驗結果的背後故事。
- 視覺化： 我們提供豐富的數據視覺化工具 Plotly，以圖表和圖形的形式呈現分析結果，使複雜的數據更容易理解。

**請按開左上方的分頁箭頭**，開始使用吧！上傳您的測驗結果，探索數據，並獲得深入的分析報告。如果您有任何問題，請隨時聯繫我們。

謝謝您選擇這個的工具，我們期待為您提供卓越的數據分析體驗！

版本 V1.0116_2024
""")
