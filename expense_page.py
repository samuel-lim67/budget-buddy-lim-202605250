import streamlit as st
from data_loader import load_budget_data, load_expense_data, save_expense_data
from budget_page import get_categories
import calendar
from datetime import date, datetime
import pandas as pd

expense = load_expense_data()
budget = load_budget_data()

selected_month = st.session_state.get("selected_budget", "")

def get_total():
    total = 0
    for entry in expense:
        if entry["month"] == selected_month:
            total += entry["amount"]
        else:
            continue
    return total

@st.dialog("Add New Expense")
def add_expense():
    category = st.selectbox("Select Category", options=categories)
    date = st.date_input("Date of Expense", value=first_day, min_value=first_day, max_value=last_day)
    description = st.text_input("Enter expense description")
    expense_amount = st.number_input("How much did you spend", min_value=0.0, step=100.0)
    if st.button("Create"):
        if not description:
            st.error("Please enter expense description!")
        elif expense_amount == 0:
            st.rerun()
        else:
            save_expense(category, date, description,expense_amount)
            st.rerun()

def save_expense(category, date, description,expense_amount):
    new_expense = {
        "date": date,
        "month": selected_month,
        "category": category,
        "description": description,
        "amount": round(expense_amount, 1),
    }

    expense.append(new_expense)
    save_expense_data(expense)
    st.toast("Expense Successfully Logged!")

def row_display(entry):
    date, category, description, amount, delete = st.columns(5)
    with date:
        st.markdown(entry["date"])
    with category:
        st.markdown(entry["category"])
    with description:
        st.markdown(entry["description"])
    with amount:
        st.markdown(f"₱{entry["amount"]:.2f}")
    with delete:
        if st.button("x", key= f"{entry["description"]}_delete"):
            pass

month_date = datetime.strptime(selected_month, "%B %Y") #gets the month+year given a selected budget, %B and %Y are format instructions on how itll interpret the entered string
first_day = date(month_date.year, month_date.month, 1)
last_day = date(month_date.year, month_date.month, calendar.monthrange(month_date.year, month_date.month)[1])

budget_allocation = get_categories(budget, selected_month)
categories = budget_allocation.keys()
allocation = budget_allocation.values()

#ACTUAL PROGRAM///////////////////////////////////////////////////////////////////
for entry in expense:
    print(entry)
if not selected_month:
    st.markdown("# Select a budget timeframe to get started!")
else:
    st.title(f"Total Expenses for {selected_month}: ₱{get_total():.2f}")

    st.divider()

    column1, column2 = st.columns([3.88, 1])
    with column2:
        st.space("large")
        if st.button("+ Add Expense"): # checks if u even have space in the budget to add a new category
            add_expense()
        st.multiselect("View Specific Category", options=categories, key="selected_categories")
    with column1:
        st.markdown(f"# List of expenses for {selected_month}")
        df = pd.DataFrame(expense)
        df = df[df["month"] == selected_month]

        df["date"] = pd.to_datetime(df["date"]).dt.date

        if not st.session_state["selected_categories"]:
            st.dataframe(df, use_container_width=True, hide_index=True, height="content", column_config=
            {
                "date": st.column_config.DateColumn(
                    "Date",
                    format="YYYY-MM-DD"
                ),
                "month": "Month",
                "category": "Category",
                "description": "Description",
                "amount": st.column_config.NumberColumn(
                    "Amount",
                    format="₱%.2f"
                )
            }
                                         )
        else:
            df = df[df["category"].isin(st.session_state["selected_categories"])]
            st.dataframe(df, use_container_width=True, hide_index=True,  height="content", column_config=
            {
                "date": st.column_config.DateColumn(
                    "Date",
                    format="YYYY-MM-DD"
                ),
                "month": "Month",
                "category": "Category",
                "description": "Description",
                "amount": st.column_config.NumberColumn(
                    "Amount",
                    format="₱%.2f"
                )
            }
                         )
