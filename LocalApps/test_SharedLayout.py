import pandas as pd
import streamlit as st
import plotly.express as px
import io

from SharedLayout import layout_class

# Test case 1: Test with include_all=False
def test_layout_class_include_all_false():
    st.session_state.class_groups = {
        "Class1": {
            "class_numbers": [1, 2, 3],
            "subjects": ["Math", "Science"],
        },
        "Class2": {
            "class_numbers": [4, 5, 6],
            "subjects": ["English", "History"],
        }
    }
    st.session_state['subjects'] = {
        "Math": {
            "idv_score": pd.DataFrame({'學號': [1, 2, 3, 4, 5, 6], 'Percentage': [0.8, 0.9, 0.7, 0.6, 0.5, 0.4]}),
            "correct_rate": lambda class_numbers, include_all: pd.DataFrame({'Question': ['Q1', 'Q2', 'Q3'], 'Percentage': [0.8, 0.9, 0.7]}),
            "error_rank": pd.DataFrame({'學號': [1, 2, 3, 4, 5, 6], 'Question': ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6'], 'Percentage': [0.8, 0.9, 0.7, 0.6, 0.5, 0.4]}),
        },
        "Science": {
            "idv_score": pd.DataFrame({'學號': [1, 2, 3, 4, 5, 6], 'Percentage': [0.7, 0.6, 0.8, 0.9, 0.5, 0.4]}),
            "correct_rate": lambda class_numbers, include_all: pd.DataFrame({'Question': ['Q1', 'Q2', 'Q3'], 'Percentage': [0.7, 0.6, 0.8]}),
            "error_rank": pd.DataFrame({'學號': [1, 2, 3, 4, 5, 6], 'Question': ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6'], 'Percentage': [0.7, 0.6, 0.8, 0.9, 0.5, 0.4]}),
        }
    }
    st.selectbox = lambda label, options: "Class1"
    st.multiselect = lambda label, options: ["Math"]
    st.number_input = lambda label, min_value, max_value, value, step: 0.7
    st.dataframe = lambda df: None
    st.plotly_chart = lambda fig: None
    st.divider = lambda: None
    st.markdown = lambda text: None
    st.write = lambda text: None
    st.download_button = lambda label, data, file_name, mime: None

    layout_class(include_all=False)

# Test case 2: Test with include_all=True
def test_layout_class_include_all_true():
    st.session_state.class_groups = {
        "Class1": {
            "class_numbers": [1, 2, 3],
            "subjects": ["Math", "Science"],
        },
        "Class2": {
            "class_numbers": [4, 5, 6],
            "subjects": ["English", "History"],
        }
    }
    st.session_state['subjects'] = {
        "Math": {
            "idv_score": pd.DataFrame({'學號': [1, 2, 3, 4, 5, 6], 'Percentage': [0.8, 0.9, 0.7, 0.6, 0.5, 0.4]}),
            "correct_rate": lambda class_numbers, include_all: pd.DataFrame({'Question': ['Q1', 'Q2', 'Q3'], 'Percentage': [0.8, 0.9, 0.7]}),
            "error_rank": pd.DataFrame({'學號': [1, 2, 3, 4, 5, 6], 'Question': ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6'], 'Percentage': [0.8, 0.9, 0.7, 0.6, 0.5, 0.4]}),
        },
        "Science": {
            "idv_score": pd.DataFrame({'學號': [1, 2, 3, 4, 5, 6], 'Percentage': [0.7, 0.6, 0.8, 0.9, 0.5, 0.4]}),
            "correct_rate": lambda class_numbers, include_all: pd.DataFrame({'Question': ['Q1', 'Q2', 'Q3'], 'Percentage': [0.7, 0.6, 0.8]}),
            "error_rank": pd.DataFrame({'學號': [1, 2, 3, 4, 5, 6], 'Question': ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6'], 'Percentage': [0.7, 0.6, 0.8, 0.9, 0.5, 0.4]}),
        }
    }
    st.selectbox = lambda label, options: "Class1"
    st.multiselect = lambda label, options: ["Math"]
    st.number_input = lambda label, min_value, max_value, value, step: 0.7
    st.dataframe = lambda df: None
    st.plotly_chart = lambda fig: None
    st.divider = lambda: None
    st.markdown = lambda text: None
    st.write = lambda text: None
    st.download_button = lambda label, data, file_name, mime: None

    layout_class(include_all=True)

# Run the test cases
test_layout_class_include_all_false()
test_layout_class_include_all_true()