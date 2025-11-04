import pandas as pd
import budget_management as bm
from data_management import *   # uses your handlers for import/view/add/edit/delete/save

# Try to import Carolina's analysis handlers (optional safeguard)
try:
    import handlers_analysis as ha
except ImportError:
    ha = None  # if the file isn't in develop yet, we'll warn the user

# ---------- Sally's budget handlers ----------

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

    # Ensure Category column exists
    if "Category" not in df.columns:
        print("⚠️ DataFrame is missing 'Category' column.")
        return df

    cats = sorted(df["Category"].dropna().unique().tolist())
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

# ---------- Small helper ----------
def ensure_df(df):
    if df is None or getattr(df, "empty", False):
        print("⚠️ Load a CSV first (option 0) before running this option.")
        return None
    return df

# ---------- Main loop ----------
def main():
    FILE_PATH = "data/transactions.csv"  # adjust if your CSV lives elsewhere
    # Option A: auto-load at start. Option B: set df=None and force user to choose 0 first.
    try:
        df = handle_import(FILE_PATH)
    except Exception:
        df = None

    while True:
        print("\n===== PERSONAL FINANCE TRACKER =====")
        print("0. Import Data")
        print("1. View All Transactions")
        print("2. View by Date Range")
        print("3. Add Transaction")
        print("4. Edit Transaction")
        print("5. Delete Transaction")
        print("6. Monthly Totals (Analysis)")          # Carolina
        print("7. Spend by Category (Analysis)")       # Carolina
        print("8. Top Spending Category (Analysis)")   # Carolina
        print("9. Set Monthly Income")                 # Sally
        print("10. Set Category Budget")               # Sally
        print("11. Check Budget Status")               # Sally
        print("13. Save and Exit")

        choice = input("Choose an option: ").strip()

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

        # ---------- Carolina's options ----------
        elif choice == "6":
            if ha is None:
                print("⚠️ Analysis handlers not available. Pull/merge analysis files first.")
            else:
                tmp = ensure_df(df)
                if tmp is not None:
                    try:
                        # Adjust name if Carolina used a different one
                        df = ha.handle_monthly_totals(tmp)
                    except AttributeError:
                        print("⚠️ Ask Carolina the exact function name for monthly totals.")
                    except Exception as e:
                        print("⚠️ Error:", e)

        elif choice == "7":
            if ha is None:
                print("⚠️ Analysis handlers not available. Pull/merge analysis files first.")
            else:
                tmp = ensure_df(df)
                if tmp is not None:
                    try:
                        df = ha.handle_spend_by_category(tmp)
                    except AttributeError:
                        print("⚠️ Ask Carolina the exact function name for spend by category.")
                    except Exception as e:
                        print("⚠️ Error:", e)

        elif choice == "8":
            if ha is None:
                print("⚠️ Analysis handlers not available. Pull/merge analysis files first.")
            else:
                tmp = ensure_df(df)
                if tmp is not None:
                    try:
                        df = ha.handle_top_spending_category(tmp)
                    except AttributeError:
                        print("⚠️ Ask Carolina the exact function name for top spending category.")
                    except Exception as e:
                        print("⚠️ Error:", e)

        # ---------- Sally's budget options ----------
        elif choice == "9":
            handle_set_income()

        elif choice == "10":
            df = handle_set_budgets(df)

        elif choice == "11":
            df = handle_check_budget(df)

        elif choice == "13":
            try:
                handle_save(df, FILE_PATH)
            except Exception:
                pass
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()