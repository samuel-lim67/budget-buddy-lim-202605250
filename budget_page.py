import streamlit as st
from data_loader import load_budget_data, load_expense_data

expense = load_expense_data()
budget = load_budget_data()

month = st.session_state.selected_month
st.title(f"Budget for {month}")
total = 0
for amount in budget:
    if amount["month"] == month:
        total += amount['planned_amount']
    else:
        continue
st.divider()


column1, column2 = st.columns([3.88,1])

with column1:
    current_budget, current_total = st.columns(2)
    with current_budget:
        st.markdown("# This Month's Budget\n\n")
    with current_total:
        st.markdown(f"# ₱{total}")
    category, amount = st.columns(2)
    with category:
        st.markdown("")
        st.write("**Category**")
        for category_ in budget:
            if category_["month"] == month:
                st.write(category_["category"])
            else:
                continue
    with amount:
        st.write("")
        st.write("**Allocated**")
        for amount in budget:
            if amount["month"] == month:
                st.write(f"₱{amount["planned_amount"]}")



with column2:
    search_category = st.text_input("Search")