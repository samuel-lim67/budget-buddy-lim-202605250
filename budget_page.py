import streamlit as st
from data_loader import load_budget_data, load_expense_data, save_budget_data

expense = load_expense_data()
budget = load_budget_data()

selected_month = st.session_state.get("selected_budget", "") #instead aof just checking the dictionary, it sazxys to getth evalue, and if it doesnt exist the default avlue is an empty list

def get_categories(): #creates a dictionary, and then checks for each month selected, if a category is already in the dictionary, it just adds money to that category, but if not it adds it to the dictioanry
    budget_allocation = {}
    for entry in budget:
        if entry["month"] in selected_month:
            if entry["category"] in budget_allocation:
                budget_allocation[entry["category"]] += entry["planned_amount"]
            else:
                budget_allocation[entry["category"]] = entry["planned_amount"]
    return budget_allocation

def total_budget():
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
    total = total_budget()
    for entry in budget: #gets the total amount of the budget used by the categories
        if entry["month"] == selected_month:
            combined_amount += entry["planned_amount"]
    return int(total-combined_amount)

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
    st.toast("Successfully added a new category!")


@st.dialog("Add New Category")
def add_category():
    remaining = remaining_budget()
    name = st.text_input("What would you like to name this category?")
    category_amount = st.number_input("How much would you like to allocate to this category?", min_value=0, max_value=remaining, step=100)

    if st.button("Create"):
        if not name.strip():
            st.error("Please enter a name for the category!")
        elif category_amount == 0:
            st.rerun()
        else:
            save_category(selected_month,name,category_amount)
            st.rerun()

def progress_bar():
    percentage_used = (total_budget() - remaining_budget()) / total_budget() #gets the percentage of budget reminaing to place into st.progress
    progressbar = st.progress(0)
    progressbar.progress(percentage_used)
    st.markdown(f"### **Budget Used**: ₱{(total_budget()-remaining_budget()):.2f}")
    st.markdown(f"### **Remaining Budget**: ₱{remaining_budget():.2f}")

#THE ACTUAL PROGRAM ///////////////////////////////////////////////////////////////////////////////////////

if not selected_month:
    st.markdown("# Select a budget timeframe to get started!")

else:
    st.title(f"Total Budget for {selected_month}: ₱{total_budget():.2f}")
    st.divider()

    column1, column2 = st.columns([3.88,1])

    with column1:
        category, amount = st.columns(2)
        budget_allocation = get_categories()
        categories = budget_allocation.keys()
        allocation = budget_allocation.values()
        st.divider()

        with category: #displays the categories
            st.markdown("## Category")
            for category in categories:
                st.markdown(category)
        with amount: #displays the amounts for each category
            st.markdown("## Amount Allocated")
            for _allocation in allocation:
                st.markdown(f"₱ {_allocation:.2f}")

    with column2:
        if st.button("+ Add Category", disabled=remaining_budget() <= 0,  help="No remaining budget available." if remaining_budget() <= 0 else None): # checks if u even have space in the budget to add a new category
            add_category()
        progress_bar()