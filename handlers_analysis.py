from data_analysis import spend_by_category, average_monthly_spend, top_spending_category

def handle_analyze_by_cat(df):
    print("\n--- Spend by Category ---")
    print(spend_by_category(df))
    return df


def handle_avg_monthly(df):
    print("\n--- Average Monthly Expense ---")
    avg = average_monthly_spend(df)
    print("Average monthly spend:", avg)
    return df


def handle_top_category(df):
    print("\n--- Top Spending Categories ---")
    print(top_spending_category(df))
    return df
