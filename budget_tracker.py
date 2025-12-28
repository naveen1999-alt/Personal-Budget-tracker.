import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import os

# ================= COLORS =================
BG_COLOR = "#FFFFFF"
BTN_ADD = "#4CAF50"       # Green (Success)
BTN_VIEW = "#9C27B0"      # Purple
BTN_SUMMARY = "#FF9800"   # Orange
BTN_SAVINGS = "#2196F3"   # Blue
INCOME_COLOR = "#4CAF50"
EXPENSE_COLOR = "#FF5733"
SAVINGS_COLOR = "#3498DB"

# ================= FILE SETUP =================
FILE_NAME = "budget_data.csv"

def initialize_file():
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=["Date", "Type", "Category", "Amount"])
        df.to_csv(FILE_NAME, index=False)

initialize_file()

# ================= FUNCTIONS =================

def add_transaction():
    date = date_entry.get()
    trans_type = type_var.get()
    category = category_entry.get()
    amount = amount_entry.get()

    if not (date and trans_type and category and amount):
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        pd.to_datetime(date)  # Date validation
        amount = float(amount)
    except:
        messagebox.showerror("Error", "Invalid date or amount!")
        return

    df = pd.read_csv(FILE_NAME)
    df.loc[len(df)] = [date, trans_type, category, amount]
    df.to_csv(FILE_NAME, index=False)

    messagebox.showinfo("Success", "Transaction added successfully!")
    clear_entries()


def clear_entries():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)


def show_transactions():
    df = pd.read_csv(FILE_NAME)
    if df.empty:
        messagebox.showinfo("Info", "No transactions available!")
        return

    window = tk.Toplevel(root)
    window.title("Transactions")
    window.geometry("500x500")

    frame = tk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for _, row in df.iterrows():
        color = INCOME_COLOR if row["Type"] == "Income" else EXPENSE_COLOR
        tk.Label(scroll_frame, text=row.to_string(index=False),
                 fg=color, padx=10, pady=5).pack()
        tk.Label(scroll_frame, text="------------------------").pack()

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


def generate_summary():
    selected_month = month_var.get()
    df = pd.read_csv(FILE_NAME)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%Y-%m')

    monthly_data = df[df['Month'] == selected_month]

    if monthly_data.empty:
        messagebox.showinfo("Info", "No data for selected month!")
        return

    summary = monthly_data.groupby('Type')['Amount'].sum()

    summary.plot(
        kind='pie',
        autopct='%1.1f%%',
        startangle=90,
        colors=[INCOME_COLOR, EXPENSE_COLOR]
    )

    plt.title(f"Monthly Summary - {selected_month}")
    plt.ylabel("")
    plt.show()


def generate_savings():
    selected_month = month_var.get()
    df = pd.read_csv(FILE_NAME)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%Y-%m')

    if selected_month not in df['Month'].values:
        messagebox.showinfo("Info", "No data for this month!")
        return

    income = df[df['Type'] == 'Income'].groupby('Month')['Amount'].sum()
    expense = df[df['Type'] == 'Expense'].groupby('Month')['Amount'].sum()

    summary_df = pd.DataFrame({
        "Income": income,
        "Expenses": expense,
        "Savings": income - expense
    }).fillna(0)

    summary_df.plot(
        kind="bar",
        color=[INCOME_COLOR, EXPENSE_COLOR, SAVINGS_COLOR]
    )

    plt.title("Monthly Income, Expenses & Savings")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.show()


# ================= GUI =================
root = tk.Tk()
root.title("Personal Budget Tracker")
root.geometry("500x550")
root.configure(bg=BG_COLOR)

tk.Label(root, text="Date (YYYY-MM-DD)", bg=BG_COLOR, font=("Arial", 12)).pack()
date_entry = tk.Entry(root, font=("Arial", 12))
date_entry.pack()

tk.Label(root, text="Transaction Type", bg=BG_COLOR, font=("Arial", 12)).pack()
type_var = ttk.Combobox(root, values=["Income", "Expense"], font=("Arial", 12))
type_var.current(0)
type_var.pack()

tk.Label(root, text="Category", bg=BG_COLOR, font=("Arial", 12)).pack()
category_entry = tk.Entry(root, font=("Arial", 12))
category_entry.pack()

tk.Label(root, text="Amount", bg=BG_COLOR, font=("Arial", 12)).pack()
amount_entry = tk.Entry(root, font=("Arial", 12))
amount_entry.pack()

tk.Button(root, text="Add Transaction", bg=BTN_ADD, fg="white",
          font=("Arial", 12), command=add_transaction).pack(pady=5)

tk.Button(root, text="View Transactions", bg=BTN_VIEW, fg="white",
          font=("Arial", 12), command=show_transactions).pack(pady=5)

tk.Label(root, text="", bg=BG_COLOR).pack()

tk.Label(root, text="Select Month (YYYY-MM)", bg=BG_COLOR, font=("Arial", 12)).pack()
month_var = tk.StringVar()
tk.Entry(root, textvariable=month_var, font=("Arial", 12)).pack()

tk.Button(root, text="Show Monthly Summary", bg=BTN_SUMMARY,
          fg="white", font=("Arial", 12), command=generate_summary).pack(pady=5)

tk.Button(root, text="Show Monthly Savings", bg=BTN_SAVINGS,
          fg="white", font=("Arial", 12), command=generate_savings).pack(pady=5)

root.mainloop()
