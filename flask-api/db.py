from dotenv import load_dotenv, find_dotenv
import os
import psycopg2

def run_sql(sql):
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

        # Execute the SQL Query
        cursor.execute(sql)
        rows = cursor.fetchall()

        # Close connection and return results
        cursor.close()
        conn.close()
        return rows

    except Exception as e:
        print("Error:", e)
