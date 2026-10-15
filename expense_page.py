import streamlit as st
from data_loader import load_budget_data, load_expense_data, save_expense_data
from budget_page import get_categories
import calendar
from datetime import date, datetime

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

@st.dialog("Delete Expense")
def delete_expense(expense):
    options = []
    for entry in expense:
        options.append(entry["description"])
    delete_item = st.selectbox("What would you like to delete?", options = options)
    st.markdown("(This cannot be undone)")
    yes, no = st.columns(2)
    with yes:
        if st.button("Confirm"):
            expense = [entry for entry in expense if entry["description"] != delete_item]
            save_expense_data(expense)
            st.toast(f"'{delete_item}' Successfully Removed")
            st.rerun()
    with no:
        if st.button("Cancel"):
            st.rerun()

@st.dialog("Edit Expense")
def edit_expense(expense):
    options = []
    for entry in expense:
        options.append(entry["description"])
    edit_item = st.selectbox("What would you like to edit?", options=options)
    category = st.selectbox("Select Category", options=categories)
    date = st.date_input("Date of Expense", value=first_day, min_value=first_day, max_value=last_day)
    description = st.text_input("Enter expense description")
    expense_amount = st.number_input("How much did you spend", min_value=0.0, step=100.0)
    yes, no = st.columns(2)
    with yes:
        if st.button("Confirm"):
            if not description:
                st.error("Please enter a valid description")
            elif expense_amount == 0:
                st.error("Please enter a valid amount")
            else:
                for entry in expense:
                    if entry["description"] == edit_item:
                        entry["description"] = description
                        entry["category"] = category
                        entry["date"] = date
                        entry["amount"] = expense_amount
                        break
                save_expense_data(expense)
                st.toast(f"'{edit_item}' Successfully Editted!")
                st.rerun()
    with no:
        if st.button("Cancel"):
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
        if st.button("- Delete Expense"):
            delete_expense(expense)
        if st.button("Edit Expense"):
            edit_expense(expense)
        st.multiselect("View Specific Category", options=categories, key="selected_categories")
    with column1:
        st.markdown(f"# List of expenses for {selected_month}")
        filtered_expense = [expenses for expenses in expense if expenses["month"] == selected_month]
        if not st.session_state["selected_categories"]:
            st.dataframe(filtered_expense, width="stretch", hide_index=True, height="content", column_config=
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
            filtered_expense = [expenses for expenses in expense if expenses["month"] == selected_month and expenses["category"] in st.session_state["selected_categories"]]
            st.dataframe(filtered_expense, use_container_width=True, hide_index=True,  height="content", column_config=
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
