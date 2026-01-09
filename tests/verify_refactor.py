
import sys
import os
import pandas as pd
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import data_loader
from src.analysis.analyzer import AssessmentAnalyzer

def test_pipeline():
    print("Starting verification pipeline...")
    
    # Use the existing excel file in the root directory
    excel_path = r"c:\Users\admin\PycharmProjects\PerformanceAnalysis\123年級社會歷地公答題狀況.xlsx"
    
    if not os.path.exists(excel_path):
        print(f"Error: Test file not found at {excel_path}")
        return

    print(f"Loading data from {excel_path}...")
    try:
        data = data_loader.process_excel_file(excel_path, datetime.now().isoformat())
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Failed to load data: {e}")
        return

    subjects = data.get('subjects')
    if not subjects:
        print("No subjects found in loaded data.")
        return
        
    print(f"Found {len(subjects)} subjects.")
    
    # Test Analysis on the first subject
    first_subject_key = list(subjects.keys())[0]
    subject = subjects[first_subject_key]
    print(f"Testing analysis for subject: {subject.name}...")
    
    analyzer = AssessmentAnalyzer(subject)
    
    try:
        results = analyzer.perform_grouping_analysis(method='一般分法(5組)')
        print("Analysis successful.")
        print("Summary stats:")
        print(results['student_data'].head())
    except Exception as e:
        print(f"Analysis failed: {e}")
        return

    print("Verification complete! The refactored components are working.")

if __name__ == "__main__":
    test_pipeline()
