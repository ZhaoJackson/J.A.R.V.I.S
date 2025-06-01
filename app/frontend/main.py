import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Hello, I'm JARVIS",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
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
tab1, tab2, tab3 = st.tabs(["Dashboard", "Health", "Finance"])

# ...existing code...

with tab1:
    st.header("Dashboard")
    
    # Create two columns for metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Health Overview")
        # Placeholder for health metrics
        st.metric("Average Sleep", "7.5 hours", "+0.5")
        st.metric("Daily Steps", "8,500", "-500")
        st.metric("Water Intake", "2.5L", "+0.5L")
    
    with col2:
        st.subheader("Finance Overview")
        # Placeholder for finance metrics
        st.metric("Monthly Income", "$5,000", "+$500")
        st.metric("Monthly Expenses", "$3,500", "-$200")
        st.metric("Savings Rate", "30%", "+5%")
    
    # Placeholder for charts
    st.subheader("Trends")
    
    # Check if date_range is valid
    try:
        start_date, end_date = date_range
        if start_date > end_date:
            st.error("Wrong date span, please choose a valid date range.")
        else:
            # Generate dates for the selected range
            dates = pd.date_range(start=start_date, end=end_date)
            n_days = len(dates)
            if n_days == 0:
                st.error("Wrong date span, please choose a valid date range.")
            else:
                # Generate sample data with the same length as dates
                chart_data = pd.DataFrame({
                    'Date': dates,
                    'Sleep': np.random.normal(7.5, 0.5, n_days),  # Mean 7.5 hours, std 0.5
                    'Steps': np.random.normal(8500, 500, n_days),  # Mean 8500 steps, std 500
                    'Expenses': np.random.normal(3500, 200, n_days)  # Mean $3500, std $200
                })
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=chart_data['Date'], y=chart_data['Sleep'], name='Sleep Hours'))
                fig.add_trace(go.Scatter(x=chart_data['Date'], y=chart_data['Steps']/1000, name='Steps (K)'))
                fig.add_trace(go.Scatter(x=chart_data['Date'], y=chart_data['Expenses']/1000, name='Expenses (K)'))
                
                fig.update_layout(
                    title="Health and Finance Trends",
                    xaxis_title="Date",
                    yaxis_title="Value",
                    hovermode="x unified"
                )
                
                st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.error("Wrong date span, please choose a valid date range.")

# ...existing code...

with tab2:
    st.header("Health Tracking")
    
    # Health data entry form
    with st.form("health_entry"):
        st.subheader("Enter Health Data")
        col1, col2 = st.columns(2)
        
        with col1:
            weight = st.number_input("Weight (kg)", min_value=0.0, max_value=500.0, step=0.1)
            sleep_hours = st.number_input("Sleep Hours", min_value=0.0, max_value=24.0, step=0.5)
            exercise_minutes = st.number_input("Exercise Minutes", min_value=0, max_value=1440, step=5)
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=0, max_value=250, step=1)
        
        with col2:
            bp_systolic = st.number_input("Blood Pressure (Systolic)", min_value=0, max_value=300, step=1)
            bp_diastolic = st.number_input("Blood Pressure (Diastolic)", min_value=0, max_value=200, step=1)
            water_intake = st.number_input("Water Intake (ml)", min_value=0, max_value=10000, step=100)
            steps = st.number_input("Steps", min_value=0, max_value=100000, step=100)
        
        mood = st.select_slider("Mood", options=["😢", "😕", "😐", "🙂", "😄"])
        notes = st.text_area("Notes")
        
        submitted = st.form_submit_button("Save Health Data")
        if submitted:
            st.success("Health data saved successfully!")

with tab3:
    st.header("Finance Management")
    
    # Finance data entry form
    with st.form("finance_entry"):
        st.subheader("Enter Financial Data")
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input("Amount", min_value=0.0, step=0.01)
            transaction_type = st.selectbox(
                "Transaction Type",
                ["Income", "Expense", "Investment", "Transfer"]
            )
            category = st.selectbox(
                "Category",
                ["Salary", "Food", "Transport", "Entertainment", "Bills", "Investment", "Other"]
            )
        
        with col2:
            account = st.text_input("Account")
            balance = st.number_input("Balance", min_value=0.0, step=0.01)
            recurring = st.selectbox(
                "Recurring",
                ["None", "Daily", "Weekly", "Monthly", "Yearly"]
            )
        
        description = st.text_area("Description")
        tags = st.text_input("Tags (comma-separated)")
        
        submitted = st.form_submit_button("Save Financial Data")
        if submitted:
            st.success("Financial data saved successfully!")

# Footer
st.markdown("---")
st.markdown("JARVIS Personal Assistant v1.0.0") 