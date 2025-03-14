from dotenv import load_dotenv, find_dotenv
import os
import psycopg2

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
    sql = """
    SELECT company_name, metric_name, metric_value
    FROM environmental_opportunity 
    WHERE metric_name = 'ENV_INVESTMENTS'
    AND company_name = 'Caixa Seguridade Participacoes SA';
    """
    cursor.execute(sql)
    rows = cursor.fetchall()

    # Print results
    for row in rows:
        print(row)

    # Close connection
    cursor.close()
    conn.close()

except Exception as e:
    print("Error:", e)
