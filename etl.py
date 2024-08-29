import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_customer_file(cur, filepath):
    """
    Process customer csv file and insert r ecords into the Postgres database
    :param cur: The current cursor
    :param filepath: The filepath that contains csv file
    :return:
    """

    df = pd.read_csv(filepath, encoding="utf-8")

    for i, row in df.iterrows():
        row.iloc[9] = None if pd.isna(row.iloc[9]) else row.iloc[9]
        cur.execute(customer_table_insert, list(row))

    print(f"Records inserted for file {filepath}")


def process_saving_file(cur, filepath):
    df = pd.read_csv(filepath, encoding="utf-8")

    for value in df.values:
        cur.execute(savings_table_insert, list(value))

    print(f"Records inserted for file {filepath}")


def process_loan_file(cur, filepath):
    df = pd.read_csv(filepath, encoding="utf-8")
    df = df.drop(columns=["Loan ID", "Credit Score", "Job"])
    for i, row in df.iterrows():
        # find salary of customer -> calculate annual income
        cif = row.iloc[0]
        cur.execute(salary_query, (cif,))
        result = cur.fetchone()
        if result:
            row.iloc[1] = result[0] * 12

        # insert data to table
        cur.execute(loans_table_insert, list(row))

    print(f"Records inserted for file {filepath}")


def process_accounts_file(cur, filepath):
    df = pd.read_csv(filepath, encoding="utf-8")

    if 'debit' in filepath:
        for i, row in df.iterrows():
            account_number, cif_number, account_type, status_code, customer_name, balance, first_balance, last_balance, income, outcome, month_income, month_outcome, last_trans_date, account_open_date, last_receive_date, last_activity_date = list(
                row)
            # check if last balance is <= 0 then continue
            if last_balance < 0:
                print(last_balance)
                continue
            # Convert 'NaN' to None for date fields
            last_trans_date = None if pd.isna(last_trans_date) else last_trans_date
            account_open_date = None if pd.isna(account_open_date) else account_open_date
            last_receive_date = None if pd.isna(last_receive_date) else last_receive_date
            last_activity_date = None if pd.isna(last_activity_date) else last_activity_date

            debit_account = [account_number, cif_number, account_type, status_code, balance, account_open_date,
                             first_balance, last_balance, income, outcome, month_income, month_outcome,
                             last_trans_date, last_receive_date, last_activity_date]
            cur.execute(debit_accounts_table_insert, debit_account)

        print(f"Records inserted for file {filepath}")
    elif 'credit' in filepath:
        df = pd.read_csv(filepath, encoding="utf-8")
        df = df.drop(columns=['Customer Name'])

        # Swapping position of CIF Number and Account Number
        col_list = list(df.columns)
        x, y = col_list.index("CIF Number"), col_list.index("Account Number")
        col_list[y], col_list[x] = col_list[x], col_list[y]
        df = df[col_list]
        for i, row in df.iterrows():
            if row.iloc[8] < 0:
                print(row.iloc[8])
                continue
            cur.execute(credit_accounts_table_insert, list(row))

        print(f"Records inserted for file {filepath}")


def process_cards_file(cur, filepath):
    df = pd.read_csv(filepath, encoding="utf-8")

    for i, row in df.iterrows():
        cur.execute(cards_table_insert, list(row))

    print(f"Records inserted for file {filepath}")


def process_transactions_file(cur, filepath):
    trans = pd.read_csv(filepath, encoding="utf-8")
    for i, row in trans.iterrows():
        # panda Series
        transaction = list(row)
        cur.execute(transactions_table_insert, transaction)
    print(f"Records inserted for file {filepath}")


def process_data(conn, cur, filepath, func):
    """
    Driver function to load data from csv files into Postgres database
    :param conn: The current connection to Postgres
    :param cur: The current cursor
    :param func: The function to call
    :return:
    """
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.csv'))
        for file in files:
            all_files.append(file)

    # print all found files
    print(f"There are {len(all_files)} files in the path {filepath}")

    # start to insert all data in filepath into Postgres
    for i, file in enumerate(all_files):
        func(cur, file)
        conn.commit()
        print(f"{i + 1}/{len(all_files)} files processed")


def main():
    conn = psycopg2.connect("host=localhost dbname=cdp360 user=postgres password=26102002 port=5433")
    cur = conn.cursor()

    # Insert customer data into Postgres
    process_data(conn=conn, cur=cur, filepath="./data/customer", func=process_customer_file)

    # Insert saving data into Postgres
    process_data(conn=conn, cur=cur, filepath="./data/saving", func=process_saving_file)

    # Insert loan data into Postgres
    process_data(conn=conn, cur=cur, filepath="./data/loan", func=process_loan_file)

    # Insert accounts into Postgres
    process_data(conn=conn, cur=cur, filepath="./data/account", func=process_accounts_file)

    # Insert cards into Postgres
    process_data(conn=conn, cur=cur, filepath="./data/card", func=process_cards_file)

    # Insert transactions into Postgres
    process_data(conn=conn, cur=cur, filepath="./data/transactions", func=process_transactions_file)


if __name__ == "__main__":
    main()
