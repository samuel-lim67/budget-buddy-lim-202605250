import streamlit as st
from data_loader import load_budget_data, load_expense_data, save_budget_data

expense = load_expense_data()
budget = load_budget_data()

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

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Budget", "temp")

with col2:
    st.metric("Total Spent", "temp")

with col3:
    st.metric("Remaining", "temp")

st.markdown(get_category_expense("Food"))