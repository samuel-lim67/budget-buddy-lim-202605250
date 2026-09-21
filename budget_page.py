import streamlit as st
from data_loader import load_budget_data, load_expense_data, save_budget_data

expense = load_expense_data()
budget = load_budget_data()

selected_months = st.session_state.get("selected_months", []) #instead aof just checking the dictionary, it sazxys to getth evalue, and if it doesnt exist the default avlue is an empty list

def get_categories():
    budget_allocation = {}
    for entry in budget:
        if entry["month"] in selected_months:
            if entry["category"] in budget_allocation:
                budget_allocation[entry["category"]] += entry["planned_amount"]
            else:
                budget_allocation[entry["category"]] = entry["planned_amount"]
    return budget_allocation

def total_budget():
    budget_allocation = get_categories()
    amounts = budget_allocation.values()
    total = 0
    for amount in amounts:
        total += amount
    return total

def save_category(month, name, category_amount):
    for entry in budget:
        if entry["month"] == month:
            income_source = entry["income_source"]
            income = entry["income"]
            break
    new_category = {
        "month": month,
        "income_source": income_source,
        "income": income,
        "category": name,
        "planned_amount": category_amount
    }

    budget.append(new_category)
    save_budget_data(budget)


@st.dialog("Add New Category")
def add_category():
    months = []
    combined_amount = 0
    for entry in budget:
        if entry["month"] in months:
            continue
        else:
            months.append(entry["month"])
    month = st.selectbox("Please select a month budget to add to", options=months)
    for entry in budget:
        if entry["month"] == month:
            combined_amount += entry["planned_amount"]
            total = entry["income"]

    remaining = int(total - combined_amount)
    name = st.text_input("What would you like to name this category?")
    category_amount = st.slider("How much would you like to allocate to this category?", min_value=None, max_value=remaining)

    if st.button("Create"):
        if name == "":
            st.error("Please enter a name for the category!")
        if category_amount == 0:
            st.rerun()
        else:
            save_category(month,name,category_amount)
            st.rerun()

if not selected_months:
    st.markdown("# Select a budget timeframe to get started!")

else:
    st.title(f"Budget for the Selected Months: ₱{total_budget()}")
    st.divider()

    column1, column2 = st.columns([3.88,1])

    with column1:
        category, amount = st.columns(2)
        budget_allocation = get_categories()
        categories = budget_allocation.keys()
        allocation = budget_allocation.values()
        with category:
            st.markdown("## Category")
            for category in categories:
                st.markdown(category)
            if st.button("+ Add Category"):
                add_category()
        with amount:
            st.markdown("## Amount Allocated")
            for _allocation in allocation:
                st.markdown(f"₱ {_allocation}")

    with column2:
        pass
