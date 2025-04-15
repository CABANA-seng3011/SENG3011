###############################################################################
#
# scores.py
#
# New tables: scores
###############################################################################

from dotenv import load_dotenv, find_dotenv
from constants import CATEGORIES, NASDAQ_100
import os
import psycopg2
import statistics

# Given a company and category, retrieve all percentiles
def get_all_metrics(company, category):
    sql = f"""
    SELECT percentile
    FROM esg_nasdaq_100
    WHERE company_name = '{company}'
    AND category = '{category}'
    """
    return sql

# Insert score
def insert_score(category, company, score):
    sql = f"""
    INSERT INTO scores (category, company_name, score)
    VALUES ('{category}', '{company}', {score});
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

    for category in CATEGORIES:
        print(f"*** Calculating scores for category: {category} ***")
        
        for company in NASDAQ_100:
            # Get percentiles
            sql = get_all_metrics(company, category)
            cursor.execute(sql)
            rows = cursor.fetchall()
            rows = [ row[0] for row in rows ]

            # Calculate score and insert
            score = statistics.fmean(rows)
            print(f"> {company}: {score}")
            sql = insert_score(category, company, score)
            cursor.execute(sql)
            conn.commit()

    # Commit the transaction, Close connection and return results
    conn.commit()
    cursor.close()
    conn.close()

except Exception as e:
    raise e
