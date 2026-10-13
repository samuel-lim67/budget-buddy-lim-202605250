import streamlit as st
from data_loader import load_budget_data, load_expense_data, save_budget_data
from budget_page import get_categories

expense = load_expense_data()
budget = load_budget_data()

selected_month = st.session_state.get("selected_budget", "")

st.title("Budget Buddy v1")
st.header("_By TheGalacticProg_")

def get_category_expense(category):
    total = 0
    for entry in expense:
        if entry["category"] == category:
            total += entry["amount"]
        else:
            continue
    return total

def category_display():
    table_row = []
    for category in categories:
        for entry in budget:
            if entry["month"] == selected_month:

                if entry["category"] == category:
                    category_ = {
                        "Category": category,
                        "Planned Amount": f"₱{entry["planned_amount"]:.2f}",
                        "Expenses": 0,
                        "Remaining": 0
                    }
                    table_row.append(category_)
                    break
                else:
                    continue

            else:
                continue
    for row in table_row:
        for entry in expense:
            if entry["month"] == selected_month:

                if entry["category"] == row["Category"]:
                    row["Expenses"] += entry["amount"]
        row["Remaining"] = remaining_calculator(row["Planned Amount"], row["Expenses"])
    return table_row

def remaining_calculator(planned_amount, expenses):
    remaining = float(planned_amount[1:]) - expenses
    return remaining

budget_allocation = get_categories(budget, selected_month)
categories = budget_allocation.keys()
allocation = budget_allocation.values()

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Budget", "temp")

with col2:
    st.metric("Total Spent", "temp")

with col3:
    st.metric("Remaining", "temp")

budget_breakdown = category_display()
st.dataframe(budget_breakdown)