from dotenv import load_dotenv, find_dotenv
import os
import psycopg2

def run_sql(sql, columns):
    """
    Established a connection to our team's AWS RDS instance, then runs a given SQL query.

    Args:
        sql (String): The SQL query
        columns ([String]): An array of column names in the SELECT statement
    """
    load_dotenv(find_dotenv())

    try:
        # Establish connection
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = []

        row = cursor.fetchone()
        while row is not None:
            rows.append(dict(zip(columns, row)))
            row = cursor.fetchone()

        # Close connection and return results
        cursor.close()
        conn.close()
        return rows

    except Exception as e:
        print("Error:", e)

def run_sql_raw(sql):
    """
    Established a connection to our team's AWS RDS instance, then runs a given SQL query.

    Args:
        sql (String): The SQL query
    """
    load_dotenv(find_dotenv())

    try:
        # Establish connection
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

        # Close connection and return results
        cursor.close()
        conn.close()
        return rows

    except Exception as e:
        print("Error:", e)
