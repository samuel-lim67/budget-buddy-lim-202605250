# Budget Buddy v1

Budget Buddy v1 is a flexible financial software/website application that allows users to see and better understand their monthly spending, create, add, and edit their budgets, and also track their expenses. It comes with a variety of features that makes managing your finances that much easier.

## Features

### 1. Dynamic Dashboard Page

Budget Buddy v1 features a dynamic dashboard page that displays a summary of the month's finances. It automatically calculates the total budget, the total amount spent, and the remaining amount in your budget after factoring in expenditures. Additionally, the left navigation sidebar includes options such as add new budget, delete a budget, and edit budget, to adding further practicality to the application.

It also comes with a custom table that displays each category's budget allocation and how much you've spent on that category. If you have exceeded that category's allocation, a bright red mark will be there to remind you to watch your spending!

Furthermore, the application also comes with a built-in pie chart, displaying what percentage of the budget a category occupies, as well as a bar graph that compares a category's allocation against its expenses.

Overall, the dashboard page clearly shows a summary of the month's finances and helps the user make better informed decisions in the future.

### 2. Budget Overview

Budget Buddy v1 features a very straightforward and easy-to-understand budget page that allows the user to set and control their budget however they want. The header displays the currently selected budget, as well as the total expected amount for that budget and the income source.

The budget page also displays the categories and the amount allocated per categories in separate columns. Notably, Budget Buddy v1 also features a popover menu that allows the user to either edit or delete the selected category. The edit and delete functions are robust, with guardrails implemented for ease of use and to minimize accidents while using these features.

The right column of the page also features a multiselect box, a slider, and an add category option. The multiselect box allows users to filter out which categories they want to see, which adds to the user control of the application. Additionally, there is a slider that displays the percentage of the budget already being used, alongside markdowns to display the numerical amounts. Finally, an add budget category option was implemented in order to give users further choices in how they want to manage their budget plan.

### 3. Expense Tracker

The expense tracker is a flexible tool that displays a user's expenses for that budget period. It displays the total expense at the very top of the page, before including a table that the user can sort in order to highlight the information that matters to them. 

Additionally, the right hand column of the page once again includes several features, such as an add expense feature, a delete expense feature, and an edit expense feature. All of these are robust features that give the user extra control over whatever they want to do within the application. Additionally, just like the budget page, the expense page contains a multiselect that allows you to see expenses per category, adding to the functionality of the application.


## Installation

### 1. Clone the Repository

Clone the repository from GitHub and navigate to the project folder.

git clone https://github.com/samuel-lim67/budget-buddy-lim-202605250.git

cd budget-buddy-lim-202605250

### 2. Create a Virtual Environment

Check if venv is already installed: python3 -m venv --help

Create a virtual environment: python3 -m venv SP1

Activate your virtual environment through your terminal. Make sure you are in the repository folder.

MacOS/Linux:
	source SP1/bin/activate

Windows:
	Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
	SP1\Scripts\activate

Install Streamlit and Matplotlib using pip.: pip install streamlit matplotlib

### 3. Run the Application

Make sure your terminal is in the project directory and your virtual environment is activated. Then run:

'streamlit run main.py' to start the application.

Streamlit will start a local development server and display a URL in the terminal. Open that URL in your browser to access Budget Buddy v1.


## Known Issues and Limitations

Due to the limitations of streamlit, certain UI features are a bit clunky, such as button sizes on the delete budget features, the buttons themselves on the navigator column on the left, and the graphics of the charts on the dashboard page.

Additionally, the expense page was not given its own popovers similar to the budget tab as it would have prevented the ability to sort the expenses just to have a nicer UI. I decided to prioritize functionality over design as I believe that having a functioning sorting system for the expense page is more meaningful than having a three-dot popover with limited sorting capabilities. 

On the graphs themselves, they don't have much meaningful control due to the nature of how streamlit handles charts, I tried my best to make them look good but without implementing more complicated code that I don't understand, I decided to keep it as is.