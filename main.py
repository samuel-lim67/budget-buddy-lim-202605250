import streamlit as st
from data_loader import load_budget_data, load_expense_data, save_budget_data
from datetime import datetime

expense = load_expense_data()
budget = load_budget_data()

st.set_page_config(layout="wide")
months = []

@st.dialog("Create New Budget")
def create_new_budget():
    col1, col2 = st.columns(2)
    with col1:
        month = st.selectbox("Please Select a Month", options=["January", "February", "March", "April","May","June","July","August","September","October","November","December"])
    with col2:
        year = st.selectbox("Please Select a Year", options= range(datetime.now().year,2100))
    source = st.text_input("Income Source")
    income = st.number_input("Income", min_value=0.0, step=100.0)
    budget_name = f"{month} {year}"
    if st.button("Create"):
        if budget_name in months:
            st.error("Budget already exists!")
        elif not source:
            st.error("Please enter an income source!")
        elif income == 0:
            st.rerun()
        else:
            budget.append({
                "month": budget_name,
                "income_source": source,
                "income": income,
                "category": "Miscellaneous",
                "planned_amount": income/2
            })
            save_budget_data(budget)
            st.toast("Successfully created a new budget!")
            st.rerun()
for entry in budget:
    if entry["month"] not in months:
        months.append(entry["month"])

with st.sidebar:
    st.radio("Please select a budget", options=months, key="selected_budget")
    if st.button("Add new budget"):
        create_new_budget()

    #st.sidebar.selectbox("Please select a budget option", options=months, key="selected_month", accept_new_options=True, persist_state="session")

pages = {"My Dashboard": [st.Page("dashboard_page.py", title="Overview"),st.Page("budget_page.py", title="Budget Overview"), st.Page("expense_page.py", title="Expense Tracker")]}

pg = st.navigation(pages)
pg.run()