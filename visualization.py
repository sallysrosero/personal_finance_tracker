import matplotlib.pyplot as plt
import pandas as pd

def plot_income_vs_spend_monthly(df):
    """Line chart: monthly income vs expense."""
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")

    income = df[df["Type"] == "Income"].groupby("Month")["Amount"].sum()
    expense = df[df["Type"] == "Expense"].groupby("Month")["Amount"].sum()

    months = sorted(set(income.index.tolist() + expense.index.tolist()))
    income = income.reindex(months, fill_value=0)
    expense = expense.reindex(months, fill_value=0)

    x = [str(m) for m in months]
    plt.figure()
    plt.plot(x, income.values, marker="o", label="Income")
    plt.plot(x, expense.values, marker="o", label="Expense")
    plt.title("Monthly Income vs Expense")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_spend_vs_budget(df, category_budgets, month=None):
    """Bar chart: spend vs (simple) budget per category."""
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    if month:  # 'YYYY-MM'
        df = df[df["Date"].dt.to_period("M") == pd.Period(month)]

    spent = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum()

    cats = sorted(set(spent.index.tolist() + list(category_budgets.keys())))
    spent_vals = [float(spent.get(c, 0.0)) for c in cats]
    budget_vals = [float(category_budgets.get(c, 0.0)) for c in cats]

    import numpy as np
    x = np.arange(len(cats))
    w = 0.35

    plt.figure()
    plt.bar(x - w/2, spent_vals, w, label="Spent")
    plt.bar(x + w/2, budget_vals, w, label="Budget")
    plt.title("Spend vs Budget" + (f" — {month}" if month else ""))
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.xticks(x, cats, rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_income_expense_pie(df, month=None):
    """Pie chart: share of income vs expense."""
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    if month:
        df = df[df["Date"].dt.to_period("M") == pd.Period(month)]

    total_income = df[df["Type"] == "Income"]["Amount"].sum()
    total_expense = df[df["Type"] == "Expense"]["Amount"].sum()

    if (total_income + total_expense) == 0:
        print("No data to plot.")
        return

    plt.figure()
    plt.pie([total_income, total_expense], labels=["Income", "Expense"], autopct="%1.1f%%", startangle=90)
    plt.title("Income vs Expense" + (f" — {month}" if month else ""))
    plt.tight_layout()
    plt.show()