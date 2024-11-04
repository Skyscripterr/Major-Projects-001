import pandas as pd 
import csv
from datetime import datetime
from data_entry import get_amount, get_category,get_date,get_description
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date","amount","category","description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        """
        Check if the CSV file exists.
        If it doesn't exist, create a new one with the correct columns.
        """
        try:
            # Try reading the CSV file
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            # If the file doesn't exist, create a new one
            # We create a DataFrame with the correct columns
            df = pd.DataFrame(columns=cls.COLUMNS)
            # Then we write it to the CSV file
            df.to_csv(cls.CSV_FILE, index=False)
        
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")
   
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)
        
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found")
        else:
            print(
                f"Transactions between {start_date.strftime(cls.FORMAT)} and {end_date.strftime(CSV.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )

            total_income = filtered_df[filtered_df["category"] =="Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] =="Expense"]["amount"].sum()
            
            print("\nSummary: ")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")
            
        return filtered_df        

def add():
    CSV.initialize_csv()
    date = get_date(
        "Enter the date of teh transaction(dd-mm-yyy) or enter todays date: ", 
        allow_default=True,
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount,category,description)


def plot_transactions(df):
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and expense chart")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transaction and a summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("enter the start date: ")
            end_date = get_date("enter the end date: ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see the plot? (y/n)").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exit")
            break
        else:
            print("invalid choice.")


if __name__ == "__main__":
    main()