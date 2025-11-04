import pandas as pd
import budget_management as bm
#print("RUNNING:", __file__)
#print("MENU VERSION: v9-11-enabled")
from data_management import *
def handle_set_income():
    """Ask the user for monthly income and store it in budget_management."""
    try:
        amount = float(input("💰 Enter your monthly income: ").strip())
        val = bm.set_monthly_income(amount)
        print(f"✅ Income saved: ${val:.2f}")
    except ValueError:
        print("⚠️ Invalid amount. Please try again.")


def handle_set_budgets(df):
    """
    Ask the user for a budget per category that exists in the DataFrame.
    Saves the dict in budget_management and returns df unchanged.
    """
    if df is None or getattr(df, "empty", True):
        print("⚠️ Load a CSV first (option 0) or use test data.")
        return df

    try:
        cats = sorted(df["Category"].dropna().unique().tolist())
    except KeyError:
        print("⚠️ DataFrame is missing 'Category' column.")
        return df

    print("\n🗂️ Budgets per category (press Enter for 0):")
    budgets = {}
    for c in cats:
        raw = input(f"  {c}: ").strip()
        try:
            budgets[c] = float(raw) if raw else 0.0
        except ValueError:
            budgets[c] = 0.0

    bm.set_category_budgets(budgets)
    print("✅ Budgets saved.")
    return df


def handle_check_budget(df):
    """
    Compute and display spent vs budget per category, with OK/WARNING/ALERT
    plus human-readable suggestions.
    """
    if df is None or getattr(df, "empty", True):
        print("⚠️ Load a CSV first (option 0).")
        return df

    status, tips = bm.compute_budget_status(df, bm.get_category_budgets())
    print("\n📊 Budget status:")
    for cat, (spent, bud, state) in status.items():
        icon = "🟢" if state == "OK" else ("🟡" if state == "WARNING" else "🔴")
        print(f"{icon} {cat}: ${spent:.2f} / ${bud:.2f} → {state}")

    print("\n💡 Suggestions:")
    for t in tips:
        print(" -", t)
    return df

FILE_PATH = "data/transactions.csv"

def main():
    df = handle_import(FILE_PATH)

    while True:
        print("\n===== PERSONAL FINANCE TRACKER =====")
        print("0. Import Data")
        print("1. View All Transactions")
        print("2. View by Date Range")
        print("3. Add Transaction")
        print("4. Edit Transaction")
        print("5. Delete Transaction")
        print("9. Set Monthly Income")
        print("10. Set Category Budget")
        print("11. Check Budget Status")
        print("13. Save and Exit")

        choice = input("Choose an option: ")

        if choice == "0":
            df = handle_import(FILE_PATH)
        elif choice == "1":
            handle_view_all(df)
        elif choice == "2":
            handle_view_by_date(df)
        elif choice == "3":
            df = handle_add(df)
        elif choice == "4":
            df = handle_edit(df)
        elif choice == "5":
            df = handle_delete(df)
        elif choice == "9":
            handle_set_income()
        elif choice == "10":
            df = handle_set_budgets(df)
        elif choice == "11":
            df = handle_check_budget(df)
        elif choice == "13":
            handle_save(df, FILE_PATH)
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
