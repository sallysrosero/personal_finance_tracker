import pandas as pd

# ---------- Core Functions ----------

def load_csv(file_path):
    """Carga un CSV y asegura el esquema correcto"""
    try:
        df = pd.read_csv(file_path)
        df = ensure_schema(df)
        print("✅ Data loaded successfully")
        return df
    except FileNotFoundError:
        print("⚠️ CSV not found, creating a new one.")
        df = pd.DataFrame(columns=["Date","Category","Description","Amount","Type"])
        return df

def ensure_schema(df):
    """Asegura que el DataFrame tenga las columnas necesarias"""
    expected_columns = ["Date","Category","Description","Amount","Type"]
    for col in expected_columns:
        if col not in df.columns:
            df[col] = ""
    return df

def save_csv(df, file_path):
    df.to_csv(file_path, index=False)
    print("✅ Data saved in CSV format.")

def view_all(df):
    if df.empty:
        print("⚠️ There are no transactions.")
    else:
        print(df)

def view_by_date_range(df, start_date, end_date):
    """Muestra transacciones entre dos fechas"""
    if df.empty:
        print("⚠️ No transactions to show.")
        return
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    filtered = df.loc[mask]
    if filtered.empty:
        print("⚠️ No transactions in this date range.")
    else:
        print(filtered)

def add_transaction(df):
    date = input("Date (YYYY-MM-DD): ")
    category = input("Category: ")
    desc = input("Description: ")
    amount = float(input("Amount: "))
    t_type = input("Type (Income/Expense): ")

    new_row = {"Date": date, "Category": category, "Description": desc,
               "Amount": amount, "Type": t_type}

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    print("✅ Transaction added.")
    return df

def edit_transaction(df):
    if df.empty:
        print("⚠️ There are no transactions to edit.")
        return df

    print(df)  
    try:
        idx = int(input("Index to edit: "))
        if 0 <= idx < len(df):
            for col in df.columns:
                new_value = input(f"{col} ({df.at[idx, col]}): ")
                if new_value:
                    df.at[idx, col] = float(new_value) if col == "Amount" else new_value
            print("✅ Transaction edited")
        else:
            print("❌ Invalid index")
    except ValueError:
        print("❌ Must enter a valid number")
    return df

def delete_transaction(df):
    if df.empty:
        print("⚠️ No transactions to delete.")
        return df

    print(df)
    try:
        idx = int(input("Index to remove: "))
        if 0 <= idx < len(df):
            df = df.drop(idx).reset_index(drop=True)
            print("✅ Deleted transaction.")
        else:
            print("❌ Invalid index.")
    except ValueError:
        print("❌ Must enter a valid number.")
    return df

def categories(df):
    """Devuelve lista única de categorías"""
    if df.empty:
        return []
    return df['Category'].unique().tolist()


# ---------- Handler Functions (para main.py) ----------

def handle_import(file_path):
    return load_csv(file_path)

def handle_view_all(df):
    view_all(df)

def handle_view_by_date(df):
    start = input("Start date (YYYY-MM-DD): ")
    end = input("End date (YYYY-MM-DD): ")
    view_by_date_range(df, start, end)

def handle_add(df):
    return add_transaction(df)

def handle_edit(df):
    return edit_transaction(df)

def handle_delete(df):
    return delete_transaction(df)

def handle_save(df, file_path):
    save_csv(df, file_path)

