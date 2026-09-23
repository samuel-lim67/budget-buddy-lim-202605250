import streamlit as st
from data_loader import load_budget_data, load_expense_data
expense = load_expense_data()
budget = load_budget_data()

st.set_page_config(layout="wide")
months = []

for entry in budget:
    if entry["month"] not in months:
        months.append(entry["month"])

with st.sidebar:
    st.radio("Please select a budget", options=months, key="selected_budget")

    #st.sidebar.selectbox("Please select a budget option", options=months, key="selected_month", accept_new_options=True, persist_state="session")

pages = {"My Dashboard": [st.Page("dashboard_page.py", title="Overview"),st.Page("budget_page.py", title="Budget Overview"), st.Page("expense_page.py", title="Expense Tracker")]}
pg = st.navigation(pages)
pg.run()