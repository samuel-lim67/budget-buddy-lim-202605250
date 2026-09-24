import streamlit as st
from data_loader import load_budget_data, load_expense_data, save_budget_data

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

#ACTUAL PROGRAM///////////////////////////////////////////////////////////////////

st.title(f"Total Expenses for {selected_month}: ₱{get_total():.2f}")

st.divider()