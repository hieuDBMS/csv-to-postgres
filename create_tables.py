import time  # Import time module for waiting
import psycopg2

from sql_queries import *


def create_database():
    """
    Establishes connection to PostgreSQL and returns the connection and cursor reference.
    :return: (cur, conn) a cursor and connection reference
    """

    # Connect to default database
    conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=26102002 port=5433")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    try:
        # Check if there are active connections to cdp360
        cur.execute("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = 'cdp360'
            AND pg_stat_activity.pid <> pg_backend_pid();
        """)

        # Wait for existing connections to terminate
        time.sleep(1)

        # Drop cdp360 if it exists
        cur.execute("DROP DATABASE IF EXISTS cdp360")

        # Create cdp360 with utf8 encoding
        cur.execute("CREATE DATABASE cdp360 WITH ENCODING 'utf-8' TEMPLATE template0")

    except psycopg2.Error as e:
        print("Error during database operations:", e)
    finally:
        # Close connection to default database
        conn.close()

    conn = psycopg2.connect("host=localhost dbname=cdp360 user=postgres password=26102002 port=5433")
    cur = conn.cursor()

    return conn, cur


def create_tables(conn, cur):
    for query in create_table_queries:
        print(query)
        cur.execute(query)
        conn.commit()


def drop_tables(conn, cur):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


# def create_triggers(conn, cur):
#     cur.execute(create_trigger_function)
#     cur.execute(create_trigger)
#     conn.commit()


def main():
    """
    Driver main function
    """

    conn, cur = create_database()

    drop_tables(conn, cur)
    print("Tables dropped successfully!!")

    create_tables(conn, cur)
    print("Tables created successfully!!")

    # create_triggers(conn, cur)
    # print("Trigger created successfully!!")

    conn.close()


if __name__ == "__main__":
    main()
