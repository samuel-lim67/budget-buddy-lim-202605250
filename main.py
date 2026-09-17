import streamlit as st
from data_loader import load_budget_data, load_expense_data

expense = load_expense_data()
budget = load_budget_data()

months = []

for entry in budget:
    if entry["month"] not in months:
        months.append(entry["month"])

st.title("Budget Buddy v1")
st.header("_by thegalacticprog_")

st.divider()

month = st.selectbox("Select a month", months)
st.caption("_Last 30 days_")

st.header(f"{month}")

column1, column2 = st.columns(2)

with column1:
    category, amount = st.columns(2)
    with category:
        st.write("**Category**")
        for category_ in budget:
            if category_["month"] == month:
                st.write(category_["category"])
            else:
                continue
        st.write("Total")
    with amount:
        st.write("**Amount**")
        total = 0
        for amount_ in budget:
            if amount_["month"] == month:
                st.write(f"₱{amount_['planned_amount']}")
                total += amount_['planned_amount']
            else:
                continue
        st.text(f"₱{total}")