###############################################################################
#
# filter_nasdaq.py
#
# This script goes through all rows in esg_hub and returns only companies
# that are in the NASDAQ-100
#
###############################################################################

from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from constants import NASDAQ_100
import os
import psycopg2

# Getting that esg data
def get_sql(company):
    sql = """
    INSERT INTO esg_nasdaq_100 (company_name, perm_id, data_type, disclosure, metric_description, metric_name, metric_unit, metric_value, metric_year, nb_points_of_observations, metric_period, provider_name, reported_date, pillar, headquarter_country, category)
    SELECT company_name, perm_id, data_type, disclosure, metric_description, metric_name, metric_unit, metric_value, metric_year, nb_points_of_observations, metric_period, provider_name, reported_date, pillar, headquarter_country, category
    FROM esg
    WHERE company_name='{}';
    """.format(company)
    return sql

def check(company):
    sql = """
    SELECT company_name, perm_id, data_type, disclosure, metric_description, metric_name, metric_unit, metric_value, metric_year, nb_points_of_observations, metric_period, provider_name, reported_date, pillar, headquarter_country, category
    FROM esg_nasdaq_100
    WHERE company_name='{}';
    """.format(company)
    return sql

def check_all():
    sql = """
    SELECT company_name, perm_id, data_type, disclosure, metric_description, metric_name, metric_unit, metric_value, metric_year, nb_points_of_observations, metric_period, provider_name, reported_date, pillar, headquarter_country, category
    FROM esg_nasdaq_100
    """
    return sql

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

    num = 1
    total_rows = 0
    for company in NASDAQ_100:
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert rows
        print(f"{num} {time}: Inserting {company}...")
        sql = get_sql(company)
        cursor.execute(sql)
        conn.commit()

        # Check rows
        print(f"{num} {time}: Checking {company}...")
        sql = check(company)
        cursor.execute(sql)
        rows = cursor.fetchall()

        total_rows += len(rows)
        if len(rows) == 0:
            print(f"{num} {time}: Found no rows for {company} :(")
        else:
            print(f"{num} {time}: Found {len(rows)} rows for {company}")

        num += 1

    # Close connection and return results
    # Check all rows
    sql = check_all()
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(f"EXPECTED: Fetched {total_rows} rows")
    print(f"ACTUAL: Fetched {len(rows)} rows")

    # Commit the transaction, Close connection and return results
    conn.commit()
    cursor.close()
    conn.close()

except Exception as e:
    raise e
