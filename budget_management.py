# budget_management.py
_income_value = None
_budgets = {}

def set_monthly_income(amount):
    """Store the user's monthly income and return it as float."""
    global _income_value
    _income_value = float(amount)
    return _income_value

def get_monthly_income():
    """Return the stored monthly income (or None)."""
    return _income_value

def set_category_budgets(budgets):
    """Store budgets per category. Expects a dict {category: amount}."""
    global _budgets
    _budgets = {str(k): float(v) for k, v in budgets.items()}
    return _budgets

def get_category_budgets():
    """Return the current category budgets dict."""
    return _budgets

def spend_vs_budget(df, budgets):
    """
    Compute total spent per category (only rows where Type == 'Expense')
    and pair it with the configured budget.
    Returns: dict {category: (spent, budget)}
    """
    totals = {}
    if df is None or df.empty:
        return totals

    exp = df[df["Type"].str.lower() == "expense"]
    for cat, grp in exp.groupby("Category"):
        spent = float(grp["Amount"].sum())
        budget = float(budgets.get(cat, 0))
        totals[cat] = (spent, budget)

    # Ensure categories present in budgets appear even if spent=0
    for cat, bud in budgets.items():
        totals.setdefault(cat, (0.0, float(bud)))

    return totals

def compute_budget_status(df, budgets, warn_threshold=0.90):
    """
    For each category, classify status as:
      - OK       : spent < warn_threshold * budget
      - WARNING  : warn_threshold * budget <= spent <= budget
      - ALERT    : spent > budget
    Returns:
      status: dict {category: (spent, budget, state)}
      suggestions: list[str]
    """
    status, suggestions = {}, []
    for cat, (spent, budget) in spend_vs_budget(df, budgets).items():
        if budget <= 0:
            state = "OK"
        elif spent > budget:
            state = "ALERT"
            suggestions.append(f"You exceeded the budget for {cat}.")
        elif spent >= warn_threshold * budget:
            state = "WARNING"
            suggestions.append(f"You're close to the limit in {cat}.")
        else:
            state = "OK"
        status[cat] = (spent, budget, state)

    if not suggestions:
        suggestions.append("Everything is under control. Great budgeting! 🎯")

    return status, suggestions

def reset_budgets():
    """Reset income and all category budgets."""
    global _income_value, _budgets
    _income_value, _budgets = None, {}
