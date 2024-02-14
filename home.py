import streamlit as st
import streamlit_antd_components as sac

from Subpages import By_Class_Analysis, By_Subject_Analysis, Upload_Excel, Generate_Report

st.set_page_config(layout="wide")


def overview():
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

版本 V1.0215_2024
""")


with st.sidebar.container():
    re_tag = sac.Tag('Redesign', color='green')
    new_tag = sac.Tag('New', color='green')
    menu = sac.menu([
        sac.MenuItem('Home', icon='house-fill', tag=[re_tag]),
        sac.MenuItem('上傳Excel檔案', description='為了保護個資，網頁關閉後資料即移除', icon='filetype-xlsx'),
        sac.MenuItem('分析工具', icon='clipboard-data', description='網頁可互動式選取', children=[
            sac.MenuItem('科任老師報表與分析', icon='bar-chart-line', description=''),
            sac.MenuItem('導師報表與分析', icon='diagram-3', description=''),
        ]),
        sac.MenuItem('輸出檔案', icon='filetype-pdf', description='固定格式分析報表', children=[
            sac.MenuItem('分科報告', icon='bar-chart-line-fill', tag=[new_tag]),
            # sac.MenuItem('分班報告', icon='diagram-3-fill', description=''),
            sac.MenuItem('分班報告', icon='cone-striped', description='', tag=[new_tag]),

        ]),
    ], open_all=True, color='blue')

if menu == 'Home':
    overview()
elif menu == '上傳Excel檔案':
    Upload_Excel.main()
elif menu == '科任老師報表與分析':
    By_Subject_Analysis.main()
elif menu == '導師報表與分析':
    By_Class_Analysis.main()
elif menu == '分科報告':
    Generate_Report.main()
elif menu == '分班報告':
    Generate_Report.tbd()
    # show_pages(
    #     [
    #         Page("home.py", "Home", ":school:"),
    #         Page("Subpages/Upload_Excel.py", "上傳Excel檔案", ":green_book:"),
    #         Page("Subpages/By_Subject_Analysis.py", "科任老師報表與分析", ":bar_chart:"),
    #         Page("Subpages/By_Class_Analysis.py", "導師專區", ":triangular_ruler:"),
    #     ]
    # )
