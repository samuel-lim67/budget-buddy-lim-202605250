import streamlit as st
from data_loader import load_budget_data, load_expense_data, save_budget_data
from budget_page import get_categories
import matplotlib.pyplot as plt

expense = load_expense_data()
budget = load_budget_data()

selected_month = st.session_state.get("selected_budget", "")

st.title("Budget Buddy v1")
st.header("_By Samuel Lim_")

bg_color = st.get_option("theme.backgroundColor") #gets the background color
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
                        "Planned Amount": entry["planned_amount"],
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

def total_budget(budget, selected_month):
    month_total = {} #dictionary that assigns a total budget for each month
    for entry in budget:
        if entry["month"] in selected_month:
            if entry["month"] in month_total:
                continue
            else:
                month_total[entry["month"]] = entry["income"]
    return month_total[selected_month]

def remaining_calculator(planned_amount, expenses):
    remaining = float(planned_amount) - expenses
    return remaining

def row_display(category, allocation, expenses, remaining):
    category_, allocation_, expenses_, remaining_ = st.columns(4)
    with category_:  # displays the categories
        st.markdown(category)
    with allocation_:  # displays the amounts for each category
        st.markdown(f"₱{allocation:.2f}")
    with expenses_:
        st.markdown(f"₱{expenses:.2f}")
    with remaining_:
        if remaining < 0:
            st.error(f"Over budget by ₱{abs(remaining):.2f}")
        else:
            st.success(f"₱{remaining:.2f} remaining")

def get_total_expense():
    total = 0
    for entry in expense:
        if entry["month"] == selected_month:
            total += entry["amount"]
        else:
            continue
    return total

def remaining_budget():
    combined_amount = 0
    total = total_budget(budget, selected_month)
    for entry in budget: #gets the total amount of the budget used by the categories
        if entry["month"] == selected_month:
            combined_amount += entry["planned_amount"]
    return int(total-combined_amount)

budget_allocation = get_categories(budget, selected_month)
categories = list(budget_allocation.keys())
allocation = list(budget_allocation.values())

month_budget = total_budget(budget, selected_month)
total_expenses = get_total_expense()
remaining_ = month_budget - total_expenses
st.divider()

leftover_budget = remaining_budget()
#ACTUAL CODE///////////////////////////////////////////////////////////////////

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Budget", value=f"₱{month_budget:.2f}")

with col2:
    st.metric("Total Spent", value=f"₱{total_expenses:.2f}")

with col3:
    st.metric("Remaining", value=f"₱{remaining_:.2f}")

st.divider()

budget_breakdown = category_display()

category_, allocation_, expenses_, remaining_ = st.columns(4)
with category_:
    st.markdown("### Category")
with allocation_:
    st.markdown("### Allocation")
with expenses_:
    st.markdown("### Expenses")
with remaining_:
    st.markdown("### Remaining")
for row in budget_breakdown:
    row_display(row["Category"], row["Planned Amount"], row["Expenses"], row["Remaining"])

if leftover_budget  > 0:
    categories.append("Unallocated")
    allocation.append(leftover_budget)
st.divider()
pie, bar = st.columns(2)

with pie:

    figure, piechart = plt.subplots()

    piechart.pie(allocation,  autopct="%1.1f%%")
    piechart.legend(categories, title="Categories",loc="center left" , bbox_to_anchor=(1, 0.5),)

    piechart.set_title("Budget Allocation")

    st.pyplot(figure)

with bar:
    st.bar_chart(budget_breakdown, x="Category", y=["Planned Amount", "Expenses"], stack=False, color=["#90EE90", "#FF8A8A"])