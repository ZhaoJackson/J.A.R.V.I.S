import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import sys
import os
import git
from pathlib import Path

# Add the parent directory to the Python path using relative path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from services.data.physical_health_tracker import PhysicalHealthTracker
from services.data.mental_health_tracker import MentalHealthTracker
from services.data.finance_tracker import FinanceTracker

# Initialize trackers
physical_tracker = PhysicalHealthTracker()
mental_tracker = MentalHealthTracker()
finance_tracker = FinanceTracker()

# Function to sync data with remote repository
def sync_with_remote():
    try:
        repo = git.Repo(os.path.dirname(parent_dir))
        
        # Add all CSV files in the output directory
        output_dir = os.path.join(os.path.dirname(parent_dir), 'output')
        for file in os.listdir(output_dir):
            if file.endswith('.csv'):
                file_path = os.path.join(output_dir, file)
                repo.index.add([file_path])
        
        # Add the database file
        db_path = os.path.join(os.path.dirname(parent_dir), 'health_finance.db')
        if os.path.exists(db_path):
            repo.index.add([db_path])
        
        # Check if there are any changes to commit
        if repo.is_dirty():
            repo.index.commit(f'Update data files - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            repo.remotes.origin.push()
            return True
        return True
    except Exception as e:
        st.error(f"Error syncing with remote: {str(e)}")
        return False

# Page configuration
st.set_page_config(
    page_title="JARVIS - Personal Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 4rem;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 1rem;
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .success-message {
        padding: 1rem;
        background-color: #dff0d8;
        border: 1px solid #d6e9c6;
        border-radius: 4px;
        color: #3c763d;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        background-color: #f2dede;
        border: 1px solid #ebccd1;
        border-radius: 4px;
        color: #a94442;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("JARVIS Controls")
st.sidebar.markdown("---")

# Date range selector
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(datetime.now() - timedelta(days=30), datetime.now()),
    max_value=datetime.now()
)

# Main content
st.title("🤖 Hello, I'm JARVIS")
st.markdown("Your AI-powered personal assistant for health and finance management")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Physical Health", "Mental Health", "Personal Finance", "Dashboard"])

# Physical Health Tab
with tab1:
    st.header("Physical Health")
    
    # Data Entry Form
    with st.form("physical_health_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            kilometers_run = st.number_input("Kilometers Run", min_value=0.0, step=0.1, key="physical_km")
            meals = st.text_input("Meals", key="physical_meals")
        with col2:
            weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1, key="physical_weight")
            fitness = st.text_input("Fitness Activities", key="physical_fitness")
        
        submitted = st.form_submit_button("Save Physical Health Data")
        if submitted:
            physical_tracker.save_daily_data(kilometers_run, meals, weight, fitness)
            st.success("Physical health data saved successfully!")

# Mental Health Tab
with tab2:
    st.header("Mental Health")
    
    # Mental Status Section
    mental_status = st.selectbox("Overall Mental Status", ["Normal", "Good", "Extremely Good", "Excellent"], key="mental_status")
    
    # Positive Things Section
    st.subheader("Positive Things Today")
    positive_thing1 = st.text_input("Positive Thing 1", key="positive_1")
    positive_thing2 = st.text_input("Positive Thing 2", key="positive_2")
    positive_thing3 = st.text_input("Positive Thing 3", key="positive_3")
    
    # New People Section
    st.subheader("New People Met Today")
    new_people_count = st.number_input("Number of New People Met", min_value=0, max_value=10, step=1, key="new_people_count")
    
    if new_people_count > 0:
        for i in range(new_people_count):
            st.markdown(f"---\nPerson {i+1}")
            col1, col2 = st.columns(2)
            with col1:
                job = st.text_input(f"Job {i+1}", key=f"job_{i}")
                sex = st.selectbox(f"Sex {i+1}", ["Male", "Female"], key=f"sex_{i}")
                graduated = st.selectbox(f"Graduated? {i+1}", ["Yes", "No"], key=f"graduated_{i}")
            with col2:
                potential_to_meet = st.selectbox(f"Potential to Meet? {i+1}", ["Yes", "No"], key=f"potential_{i}")
                interest = st.text_input(f"Interest {i+1}", key=f"interest_{i}")
    
    # Challenges Section
    st.subheader("Challenges")
    challenging_thing = st.text_area("Most Challenging Thing Today", key="challenge")
    impact = st.text_area("Impact of the Challenge", key="impact")
    
    if st.button("Save Mental Health Data", key="save_mental"):
        mental_tracker.save_daily_data(
            mental_status,
            [positive_thing1, positive_thing2, positive_thing3],
            challenging_thing,
            impact
        )
        if new_people_count > 0:
            for i in range(new_people_count):
                mental_tracker.save_new_person(job, sex, graduated, potential_to_meet, interest)
        st.markdown('<div class="success-message">Mental health data saved successfully!</div>', unsafe_allow_html=True)
        if sync_with_remote():
            st.markdown('<div class="success-message">Data synchronized with remote repository.</div>', unsafe_allow_html=True)

# Personal Finance Tab
with tab3:
    st.header("Personal Finance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        amount = st.number_input("Amount", min_value=0.0, step=0.01, key="finance_amount")
        transaction_type = st.selectbox("Transaction Type", ["Expense", "Income", "Transfer"], key="transaction_type")
        category = st.selectbox("Category", ["Food", "Transport", "Entertainment"], key="category")
    
    with col2:
        card_owner = st.selectbox("Card Owner", ["Me", "Family"], key="card_owner")
        if card_owner == "Me":
            card_type = st.selectbox("Card Type", ["Debit", "Credit"], key="card_type")
        else:
            card_type = "Credit"
        debit_total = st.number_input("Total Amount in Debit Card", min_value=0.0, step=0.01, key="debit_total")
        credit_total = st.number_input("Total Balance in Credit Card", min_value=0.0, step=0.01, key="credit_total")
    
    if st.button("Save Financial Data", key="save_finance"):
        finance_tracker.save_daily_data(
            amount,
            transaction_type,
            category,
            card_owner,
            debit_total,
            credit_total
        )
        st.markdown('<div class="success-message">Financial data saved successfully!</div>', unsafe_allow_html=True)
        if sync_with_remote():
            st.markdown('<div class="success-message">Data synchronized with remote repository.</div>', unsafe_allow_html=True)

# Dashboard Tab
with tab4:
    st.header("Dashboard")
    
    # Date range selector
    date_range = st.date_input(
        "Select Date Range",
        value=(datetime.now() - timedelta(days=30), datetime.now()),
        max_value=datetime.now(),
        key="dashboard_date_range"
    )
    
    # New People Trend
    st.subheader("New People Trend")
    new_people_data = mental_tracker.get_new_people_history()
    if not new_people_data.empty:
        st.line_chart(new_people_data.set_index('date')['new_people_count'])
    
    # Weight Change Trend
    st.subheader("Weight Change Trend")
    weight_data = physical_tracker.get_weight_history()
    if not weight_data.empty:
        st.line_chart(weight_data.set_index('date')['weight'])
    
    # Transaction Frequency Trend
    st.subheader("Transaction Frequency Trend")
    transaction_data = finance_tracker.get_transaction_history()
    if not transaction_data.empty:
        st.line_chart(transaction_data.set_index('date')['transaction_count'])

# Footer
st.markdown("---")
st.markdown("JARVIS Personal Assistant v1.0.0") 