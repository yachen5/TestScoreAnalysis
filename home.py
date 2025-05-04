import streamlit as st
import streamlit_antd_components as sac

from Subpages import By_Class_Analysis, By_Subject_Analysis, Upload_Excel, Generate_Report

# Constants for tags
RE_TAG = sac.Tag('Redesign', color='green')
NEW_TAG = sac.Tag('New', color='green')


def overview():
    st.title("📊 Welcome to the Data Analysis Platform!")
    st.subheader("Analyze your test results with ease and precision.")
    st.markdown("""
    ---
    **Features:**
    - **📂 Upload Files**: Easily upload your test results in Excel format.
    - **📈 Data Analysis**: Perform detailed analysis using powerful tools.
    - **📊 Visualization**: Gain insights with interactive visualizations.

    **How to Get Started:**
    1. Use the **sidebar menu** to navigate.
    2. Upload your test results.
    3. Explore the data and generate reports.

    ---
    **Need Help?** Contact us at [support@example.com](mailto:support@example.com).
    """, unsafe_allow_html=True)
    st.info("Version: V2.0303_2025")


def create_sidebar_menu():
    """Creates the sidebar menu."""
    return sac.menu([
        sac.MenuItem('🏠 Home', icon='house-fill', tag=[RE_TAG]),
        sac.MenuItem('📂 Upload Excel File', description='Data is removed after the session ends', icon='filetype-xlsx'),
        sac.MenuItem('🛠 Analysis Tools', icon='clipboard-data', description='Interactive selection available',
                     children=[
                         sac.MenuItem('📊 Subject Report & Analysis', icon='bar-chart-line'),
                         sac.MenuItem('📋 Class Report & Analysis', icon='diagram-3'),
                     ]),
        sac.MenuItem('📤 Export Files', icon='filetype-pdf', description='One-click export of formatted reports',
                     children=[
                         sac.MenuItem('📈 Subject Report', icon='bar-chart-line-fill'),
                         sac.MenuItem('📊 Class Report', icon='cone-striped'),
                         sac.MenuItem('📋 Full Grade Report', icon='cone-striped',
                                      description='Overall performance review', tag=[NEW_TAG]),
                     ]),
    ], open_all=True, color='blue')


def handle_menu_selection(menu):
    """Handles the menu selection."""
    menu_actions = {
        '🏠 Home': overview,
        '📂 Upload Excel File': Upload_Excel.main,
        '📊 Subject Report & Analysis': By_Subject_Analysis.main,
        '📋 Class Report & Analysis': By_Class_Analysis.main,
        '📈 Subject Report': Generate_Report.main,
        '📊 Class Report': Generate_Report.by_class_report,
        '📋 Full Grade Report': Generate_Report.tbd,
    }
    action = menu_actions.get(menu)
    if action:
        action()


# Main application logic
with st.sidebar.container():
    st.sidebar.title("📂 Navigation")
    menu = create_sidebar_menu()

handle_menu_selection(menu)
