from data_management import *

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
        elif choice == "13":
            handle_save(df, FILE_PATH)
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
