# Drop tables
customer_table_drop = "DROP TABLE IF EXISTS customers"
saving_table_drop = "DROP TABLE IF EXISTS savings"
loan_table_drop = "DROP TABLE IF EXISTS loans"
debit_accounts_table_drop = "DROP TABLE IF EXISTS debit_accounts"
credit_accounts_table_drop = "DROP TABLE IF EXISTS credit_accounts"
cards_table_drop = "DROP TABLE IF EXISTS cards"
transactions_table_drop = "DROP TABLE IF EXISTS transactions"


customer_table_create = (
    """
    CREATE TABLE IF NOT EXISTS customers(
        cif INT CONSTRAINT cif_pk PRIMARY KEY,
        fullname VARCHAR(200),
        address VARCHAR(200),
        mobile VARCHAR(20),
        martial_status VARCHAR(20),
        dependents VARCHAR(5),
        cust_type VARCHAR(20),
        birthdate DATE,
        sex VARCHAR(10),
        organization VARCHAR(200),
        job VARCHAR(50),
        experience INT CHECK(experience>=0),
        salary INT CHECK(salary>=0),
        existing_time INT NOT NULL CHECK(existing_time>=0),
        credit_score INT NOT NULL CHECK (credit_score>=0)
    )
    """
)

saving_table_create = (
    """
    CREATE TABLE IF NOT EXISTS savings(
        saving_id SERIAL CONSTRAINT saving_pk PRIMARY KEY,
        cif INT REFERENCES customers(cif),
        balance NUMERIC CHECK (balance>=0),
        ccycd VARCHAR(20),
        subscription_type VARCHAR(200),
        opendate DATE,
        duedate DATE,
        duration VARCHAR(20),
        status VARCHAR(10),
        allow_withdraw VARCHAR(5),
        updatedate DATE
    )
    """
)

loan_table_create = (
    """
    CREATE TABLE IF NOT EXISTS loans(
        loan_id SERIAL CONSTRAINT loan_pk PRIMARY KEY,
        cif INT REFERENCES customers(cif),
        annual_income NUMERIC CHECK (annual_income>=0),
        purpose VARCHAR(20),
        home_ownership VARCHAR(20),
        loan_amount NUMERIC CHECK (loan_amount>=0),
        loan_date DATE,
        due_date DATE,
        loan_term INT CHECK (loan_term>=0),
        monthly_debt NUMERIC CHECK (monthly_debt>=0),
        years_of_credit_history INT CHECK (years_of_credit_history>=0),
        interest_rate FLOAT CHECK (interest_rate>=0),
        total_paid NUMERIC CHECK (total_paid>=0),
        months_since_last_delinquency INT CHECK (months_since_last_delinquency>=0)
    )
    """
)

debit_account_table_create = (
    """
    CREATE TABLE IF NOT EXISTS debit_accounts(
        account_number NUMERIC CONSTRAINT debit_pk PRIMARY KEY CHECK (account_number>=0),
        cif INT REFERENCES customers(cif),
        account_type VARCHAR(20),
        status_code VARCHAR(20),
        balance NUMERIC CHECK (balance>=0),
        open_account_date DATE,
        first_balance NUMERIC CHECK (first_balance>=0),
        last_balance NUMERIC CHECK (last_balance>=0),
        income NUMERIC CHECK (income>=0),
        outcome NUMERIC CHECK (outcome>=0),
        month_income NUMERIC CHECK (month_income>=0),
        month_outcome NUMERIC CHECK (month_outcome>=0),
        last_trans_date DATE CHECK (last_trans_date >= open_account_date),
        last_receive_date DATE,
        last_activity_date DATE
    )
    """
)

credit_account_table_create = (
    """
    CREATE TABLE IF NOT EXISTS credit_accounts(
        account_number NUMERIC CONSTRAINT credit_pk PRIMARY KEY CHECK (account_number>=0),
        cif INT REFERENCES customers(cif),
        card_type VARCHAR(20),
        account_type VARCHAR(20),
        status_code VARCHAR(20),
        open_account_date DATE,
        credit_limit NUMERIC CHECK (credit_limit>=0),
        current_balance NUMERIC CHECK (current_balance>=0),
        available_credit NUMERIC CHECK (available_credit>=0),
        payment_due DATE,
        max_payment NUMERIC CHECK (max_payment>=0),
        last_payment_date DATE,
        last_late_payment_date DATE,
        late_payment_count INT CHECK(late_payment_count>=0),
        monthly_balance_incurred NUMERIC CHECK (monthly_balance_incurred>=0),
        previous_cycle_balance NUMERIC CHECK (previous_cycle_balance>=0),
        previous_cycle_interest NUMERIC CHECK (previous_cycle_interest>=0)
    )
    """
)

card_table_create = (
    """
    CREATE TABLE IF NOT EXISTS cards(
        card_id NUMERIC CONSTRAINT card_pk PRIMARY KEY CHECK (card_id>=0),
        cif INT REFERENCES customers(cif),
        card_type VARCHAR(20),
        account_number NUMERIC CHECK (account_number>=0),
        card_brand VARCHAR(20),
        card_product_name VARCHAR(100),
        issue_date DATE,
        expiry_date DATE,
        status VARCHAR(20)
    )
    """
)

transactions_table_create = (
    """
    CREATE TABLE IF NOT EXISTS transactions(
        trans_id VARCHAR(50) CONSTRAINT trans_pk PRIMARY KEY, 
        cif_number INT REFERENCES customers(cif), 
        transaction_date DATE, 
        business_date DATE, 
        trans_type VARCHAR(20) CHECK (trans_type IN ('Credit', 'Debit', 'Direct')),
        status VARCHAR(20),
        account_number NUMERIC, 
        recipient_account_number NUMERIC,
        trans_amount BIGINT
    )
    """
)

# INSERT RECORDS
customer_table_insert = ("""
     INSERT INTO customers VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""")

savings_table_insert = (
    """
    INSERT INTO savings VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
    """
)

loans_table_insert = ("""
    INSERT INTO loans VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""")
debit_accounts_table_insert = (
    """
    INSERT INTO debit_accounts VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
)

credit_accounts_table_insert = (
    """
    INSERT INTO credit_accounts VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
)

cards_table_insert = ("""
    INSERT INTO cards VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
""")

transactions_table_insert = (
    """
    INSERT INTO transactions VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
)

# FIND SALARY OF CUSTOMER
salary_query = ("""
    SELECT salary
    FROM customers
    WHERE cif = %s
""")

# QUERY LISTS
create_table_queries = [customer_table_create, saving_table_create, loan_table_create, debit_account_table_create,
                        credit_account_table_create, card_table_create, transactions_table_create]

drop_table_queries = [saving_table_drop, loan_table_drop, debit_accounts_table_drop, credit_accounts_table_drop,
                      customer_table_drop, cards_table_drop, transactions_table_drop]
