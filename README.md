# Personal-Budget-Tracker
The Personal Budget Tracker is a Python-based financial management tool that allows users to efficiently track income, expenses, and savings in an interactive and user-friendly way. The application provides essential budgeting features such as transaction tracking, monthly summaries, graphical reports, and savings analysis to help users manage their finances effectively. Using Tkinter for the graphical user interface (GUI), Pandas for data handling, and Matplotlib for data visualization, the tracker ensures a smooth and intuitive experience. Transactions are stored in a CSV file, making data storage simple yet effective.
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import os

# File for storing transactions
FILE_NAME = "budget_data.csv"

# Ensure the CSV file exists
def initialize_file():
    """Check if the CSV file exists; if not, create it with necessary columns."""
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=["Date", "Type", "Category", "Amount"])
        df.to_csv(FILE_NAME, index=False)

initialize_file()

# Function to add transaction
def add_transaction():
    """Add a new transaction to the CSV file."""
    date = date_entry.get()
    trans_type = type_var.get()
    category = category_entry.get()
    amount = amount_entry.get()
    
    if not (date and trans_type and category and amount):
        messagebox.showerror("Error", "All fields are required!")
        return
    
    try:
        amount = float(amount)  # Ensure amount is a valid number
    except ValueError:
        messagebox.showerror("Error", "Invalid amount!")
        return
    
    df = pd.read_csv(FILE_NAME)
    df.loc[len(df)] = [date, trans_type, category, amount]  # Append new transaction
    df.to_csv(FILE_NAME, index=False)  # Save back to file
    messagebox.showinfo("Success", "Transaction added successfully!")
    clear_entries()

# Function to clear entry fields
def clear_entries():
    """Clear all input fields."""
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

# Function to show transaction data
def show_transactions():
    df = pd.read_csv(FILE_NAME)
    if df.empty:
        messagebox.showinfo("Info", "No transactions available!")
        return
    
    transaction_window = tk.Toplevel(root)
    transaction_window.title("View Transactions")
    transaction_window.geometry("500x500")
    
    frame = tk.Frame(transaction_window)
    frame.pack(fill=tk.BOTH, expand=True)
    
    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    for index, row in df.iterrows():
        tk.Label(scrollable_frame, text=row.to_string(index=False), padx=10, pady=5).pack()
        tk.Label(scrollable_frame, text="--------------------------------").pack()
    
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Function to generate monthly summary
def generate_summary():
    selected_month = month_var.get()
    df = pd.read_csv(FILE_NAME)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%Y-%m')
    monthly_data = df[df['Month'] == selected_month]
    
    if monthly_data.empty:
        messagebox.showinfo("Info", "No data available for the selected month!")
        return
    
    summary = monthly_data.groupby(['Type'])['Amount'].sum()
    summary.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#FF5733'])
    plt.title(f"Monthly Summary for {selected_month}")
    plt.ylabel('')
    plt.show()

# Function to generate savings chart
def generate_savings():
    selected_month = month_var.get()
    df = pd.read_csv(FILE_NAME)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%Y-%m')
    
    if selected_month not in df['Month'].values:
        messagebox.showinfo("Info", "No details of this month have been added!")
        return
    
    income = df[df['Type'] == 'Income'].groupby('Month')['Amount'].sum()
    expenses = df[df['Type'] == 'Expense'].groupby('Month')['Amount'].sum()
    savings = income - expenses
    
    summary_df = pd.DataFrame({'Income': income, 'Expenses': expenses, 'Savings': savings}).fillna(0)
    summary_df.plot(kind='bar', stacked=False, color=['#4CAF50', '#FF5733', '#3498db'])
    plt.title("Monthly Income, Expenses, and Savings")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.legend()
    plt.show()

# GUI Setup
root = tk.Tk()
root.title("Personal Budget Tracker")  # Window title
root.geometry("500x500")  # Window size
root.configure(bg='white')  # Background color set to white

# Labels and Entries
tk.Label(root, text="Date (YYYY-MM-DD):", bg='white', fg='black', font=("Arial", 12)).pack()
date_entry = tk.Entry(root, font=("Arial", 12))
date_entry.pack()

tk.Label(root, text="Transaction Type:", bg='white', fg='black', font=("Arial", 12)).pack()
type_var = ttk.Combobox(root, values=["Income", "Expense"], font=("Arial", 12))
type_var.pack()
type_var.current(0)  # Set default selection

tk.Label(root, text="Category:", bg='white', fg='black', font=("Arial", 12)).pack()
category_entry = tk.Entry(root, font=("Arial", 12))
category_entry.pack()

tk.Label(root, text="Amount:", bg='white', fg='black', font=("Arial", 12)).pack()
amount_entry = tk.Entry(root, font=("Arial", 12))
amount_entry.pack()

# Add Transaction Button
tk.Button(root, text="Add Transaction", command=add_transaction, font=("Arial", 12), bg='#4CAF50', fg='white').pack(pady=5)

# View Transactions Button
tk.Button(root, text="View Transactions", command=show_transactions, font=("Arial", 12), bg='#9C27B0', fg='white').pack(pady=5)

# Space between View Transactions and Select Month
tk.Label(root, text="", bg='white').pack()

# Select Month Dropdown
tk.Label(root, text="Select Month (YYYY-MM):", bg='white', fg='black', font=("Arial", 12)).pack()
month_var = tk.StringVar()
month_entry = tk.Entry(root, textvariable=month_var, font=("Arial", 12))
month_entry.pack()

# Generate Summary Button
tk.Button(root, text="Show Monthly Summary", command=generate_summary, font=("Arial", 12), bg='#FF9800', fg='white').pack(pady=5)

# Generate Savings Button
tk.Button(root, text="Show Monthly Savings", command=generate_savings, font=("Arial", 12), bg='#2196F3', fg='white').pack(pady=5)

# Run the application
root.mainloop()
