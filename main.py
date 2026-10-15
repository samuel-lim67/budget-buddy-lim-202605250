import streamlit as st
from discord.ui.select import selected_values

from data_loader import load_budget_data, load_expense_data, save_budget_data, save_expense_data
from datetime import datetime

expense = load_expense_data()
budget = load_budget_data()
selected_month = st.session_state.get("selected_budget", "")

st.set_page_config(layout="wide")
months = []

def total_budget(budget, selected_month):
    month_total = {} #dictionary that assigns a total budget for each month
    for entry in budget:
        if entry["month"] in selected_month:
            if entry["month"] in month_total:
                continue
            else:
                month_total[entry["month"]] = entry["income"]
    return month_total[selected_month]

def remaining_budget():
    combined_amount = 0
    total = total_budget(budget, selected_month)
    for entry in budget: #gets the total amount of the budget used by the categories
        if entry["month"] == selected_month:
            combined_amount += entry["planned_amount"]
    return int(total-combined_amount)

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

@st.dialog("Delete a Budget")
def delete_budget(budget, expense):
    options = []
    for entry in budget:
        if entry["month"] in options:
            continue
        else:
            options.append(entry["month"])
    delete_month = st.selectbox("Select a Budget", options = options)
    st.markdown("Are you sure you want to delete this budget? ")
    st.markdown("(This cannot be undone)")
    yes, no = st.columns(2)
    with yes:
        if st.button("Yes"):
            budget = [entry for entry in budget if entry["month"] != delete_month]
            save_budget_data(budget)
            expense = [entry for entry in expense if entry["month"] != delete_month]
            save_expense_data(expense)
            st.success(f"{delete_month} budget deleted!")
            st.rerun()

    with no:
        if st.button("No"):
            st.rerun()

def save_budget_changes(edit_month, new_budget_month, amount):
    for entry in budget:
        if entry["month"] == edit_month:
            entry["month"] = f"{new_budget_month}"
            entry["income"] = amount

        else:
            continue
    save_budget_data(budget)
    st.toast("Successfully Editted Budget!")
    st.rerun()

@st.dialog("Delete a Budget")
def edit_budget(budget, expense):
    options = []
    for entry in budget:
        if entry["month"] in options:
            continue
        else:
            options.append(entry["month"])
    edit_month = st.selectbox("Select a Budget", options = options)
    for entry in budget:
        if entry["month"] == edit_month:
            budget_amount = entry["income"]
        else:
            continue
    st.markdown("What would you like to edit?")
    col1, col2 = st.columns(2)
    with col1:
        month = st.selectbox("Month",options=["January", "February", "March", "April", "May", "June", "July", "August","September", "October", "November", "December"])
    with col2:
        year = st.selectbox("Year", options=range(datetime.now().year, 2100))
    amount = st.number_input("Income", min_value=0.0, step=100.0, value=float(budget_amount))
    yes, no = st.columns(2)
    new_budget_month = f"{month} {year}"

    with yes:
        if st.button("Confirm"):
            for entry in budget:
                if entry["month"] == new_budget_month or new_budget_month == edit_month:
                    st.error(f"A budget for {new_budget_month} already exists!")
                    break
            if (total_budget(budget, selected_month)-remaining_budget()) > amount:
                st.error("This will be less than the currently allocated budget for that month!")
            else:
                save_budget_changes(edit_month, new_budget_month, amount)
    with no:
        if st.button("Cancel"):
            st.rerun()

with st.sidebar:
    st.radio("Please select a budget", options=months, key="selected_budget")
    if st.button("+ Add new budget"):
        create_new_budget()
    if st.button("-️ Delete Budget"):
        delete_budget(budget, expense)
    if st.button("Edit Budget"):
        edit_budget(budget, expense)

    #st.sidebar.selectbox("Please select a budget option", options=months, key="selected_month", accept_new_options=True, persist_state="session")

pages = {"My Dashboard": [st.Page("dashboard_page.py", title="Overview"),st.Page("budget_page.py", title="Budget Overview"), st.Page("expense_page.py", title="Expense Tracker")]}

pg = st.navigation(pages)
pg.run()