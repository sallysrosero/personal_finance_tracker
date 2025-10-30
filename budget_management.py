# budget_management.py
_income_value = None
_budgets = {}

def set_monthly_income(amount):
    global _income_value
    _income_value = float(amount)
    return _income_value

def get_monthly_income():
    return _income_value

def set_category_budgets(budgets):
    global _budgets
    _budgets = {str(k): float(v) for k, v in budgets.items()}
    return _budgets

def get_category_budgets():
    return _budgets

def spend_vs_budget(df, budgets):
    totals = {}
    if df is None or df.empty:
        return totals
    exp = df[df["Type"].str.lower() == "expense"]
    for cat, grp in exp.groupby("Category"):
        spent = float(grp["Amount"].sum())
        budget = float(budgets.get(cat, 0))
        totals[cat] = (spent, budget)
    return totals

def compute_budget_status(df, budgets, warn_threshold=0.90):
    status, suggestions = {}, []
    for cat, (spent, budget) in spend_vs_budget(df, budgets).items():
        if budget <= 0:
            state = "OK"
        elif spent > budget:
            state = "ALERT";   suggestions.append(f"Superaste el presupuesto de {cat}.")
        elif spent >= warn_threshold * budget:
            state = "WARNING"; suggestions.append(f"Estás cerca del límite en {cat}.")
        else:
            state = "OK"
        status[cat] = (spent, budget, state)
    if not suggestions:
        suggestions.append("Todo bajo control. ¡Buen manejo! 🎯")
    return status, suggestions

def reset_budgets():
    global _income_value, _budgets
    _income_value, _budgets = None, {}
