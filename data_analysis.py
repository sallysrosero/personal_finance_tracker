import pandas as pd

#This is for my data analyst girls

def total_income(df):
    """Return the total income."""
    income = df[df["Type"] == "Income"]["Amount"].sum()
    return income


def total_expense(df):
    """Return the total expense."""
    expense = df[df["Type"] == "Expense"]["Amount"].sum()
    return expense


def spend_by_category(df):
    """Show how much money was spent in each category."""
    expenses = df[df["Type"] == "Expense"]
    result = expenses.groupby("Category")["Amount"].sum()
    return result


def average_monthly_spend(df):
    """Return the average monthly expense."""
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")
    monthly = df[df["Type"] == "Expense"].groupby("Month")["Amount"].sum()
    return monthly.mean()


def top_spending_category(df, n=3):
    """Return the top spending categories."""
    expenses = spend_by_category(df)
    return expenses.sort_values(ascending=False).head(n)