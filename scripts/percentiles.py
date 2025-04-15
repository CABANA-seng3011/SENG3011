###############################################################################
#
# percentiles.py
#
# New column: percentiles
# To show a company's rank or score for a given metric
# Eg, if a company's percentile in WASTE_RECYCLED is 0.981, then that company
# performs better for the WASTE_RECYCLED than 98% of other companies in our dataset
###############################################################################

from dotenv import load_dotenv, find_dotenv
from constants import ESG_METRICS
import os
import psycopg2
import pandas as pd

# Get ideal (high/low) and data type
def get_ideal(metric):
    sql = """
    SELECT ideal, data_type
    FROM metrics
    WHERE metric_name = '{}'
    """.format(metric)
    return sql

# Get companies + values for a certain metric
def get_companies_and_values(metric):
    sql = """
    SELECT company_name, metric_value
    FROM esg_nasdaq_100
    WHERE metric_name = '{}'
    """.format(metric)
    return sql

def check_results(metric, order):
    sql = """
    SELECT company_name, metric_name, metric_value, percentile
    FROM esg_nasdaq_100
    WHERE metric_name = '{}'
    ORDER BY percentile {}
    LIMIT 3
    """.format(metric, order)
    return sql

# Set percentile column
def set_percentile(percentile, company, metric, value):
    sql = """
    UPDATE esg_nasdaq_100
    SET percentile = {}
    WHERE company_name = '{}' 
    AND metric_name = '{}' 
    AND metric_value = '{}'
    """.format(percentile, company, metric, value)
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

    for metric in ESG_METRICS:
        print(f"##### Adding percentile for metric: {metric} #####")

        sql = get_ideal(metric)
        cursor.execute(sql)
        res = cursor.fetchone()
        ideal = res[0].lower()
        type = res[1].lower()

        # Get all companies + values for the metric
        sql = get_companies_and_values(metric)
        cursor.execute(sql)
        rows = cursor.fetchall()
        print(f"Ideal value: {ideal} | Data Type: {type} | {len(rows)} companies to compare")
        
        if type == "float":
            # Create data frame
            df = pd.DataFrame(rows, columns=["company_name", "metric_value"])
            ascending = True if ideal == "high" else False
            df = df.sort_values("metric_value", ascending=ascending).reset_index(drop=True)
            df["percentile"] = df.index / (len(df) - 1)

            # Set percentile col
            for _, row in df.iterrows():
                sql = set_percentile(row["percentile"], row["company_name"], metric, row["metric_value"])
                cursor.execute(sql)
            conn.commit()
        
        else:
            # Create data frame
            df = pd.DataFrame(rows, columns=["company_name", "metric_value"])
            # count_one = (df["metric_value"] == 1).sum()
            # count_zero = (df["metric_value"] == 0).sum()
            # total = len(df)
            
            # Initialize the percentile column
            df["percentile"] = None

            if ideal == "high": # Ideal is high -- 1 is ideal
                df.loc[df["metric_value"] == 1, "percentile"] = 1
                df.loc[df["metric_value"] == 0, "percentile"] = 0

            elif ideal == "low": # Ideal is high -- 0 is ideal
                df.loc[df["metric_value"] == 1, "percentile"] = 0
                df.loc[df["metric_value"] == 0, "percentile"] = 1
            
            # Set percentile col
            for _, row in df.iterrows():
                sql = set_percentile(row["percentile"], row["company_name"], metric, row["metric_value"])
                cursor.execute(sql)
            conn.commit()
        
        # Check results
        sql_min = check_results(metric, "ASC")
        cursor.execute(sql_min)
        min_row = cursor.fetchmany(3)
        sql_max = check_results(metric, "DESC")
        cursor.execute(sql_max)
        max_row = cursor.fetchmany(3)

        print("Bottom 3 percentiles:")
        for row in min_row:
            print(f"> {row[0]} | {row[1]} | {row[2]} | {row[3]}")
        print("Top 3 percentiles:")
        for row in max_row:
            print(f"> {row[0]} | {row[1]} | {row[2]} | {row[3]}")
        print("")

    # Commit the transaction, Close connection and return results
    conn.commit()
    cursor.close()
    conn.close()

except Exception as e:
    raise e
