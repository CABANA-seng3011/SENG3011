###############################################################################
#
# check_nasdaq.py
#
# This script goes through the nasdaq-100 table and output:
# - Companies with > 96 metrics (Too many metrics)
# - Metrics that not all companies have data on
#
###############################################################################

from dotenv import load_dotenv, find_dotenv
from constants import NASDAQ_100, ESG_METRICS
import os
import psycopg2

def check_company(company):
    sql = """
    SELECT company_name, perm_id, data_type, disclosure, metric_description, metric_name, metric_unit, metric_value, metric_year, nb_points_of_observations, metric_period, provider_name, reported_date, pillar, headquarter_country, category
    FROM esg_nasdaq_100
    WHERE company_name='{}';
    """.format(company)
    return sql

def delete_company(company):
    sql = """
    DELETE FROM esg_nasdaq_100
    WHERE company_name='{}';
    """.format(company)
    return sql

def check_metric(metric):
    sql = """
    SELECT company_name, perm_id, data_type, disclosure, metric_description, metric_name, metric_unit, metric_value, metric_year, nb_points_of_observations, metric_period, provider_name, reported_date, pillar, headquarter_country, category
    FROM esg_nasdaq_100
    WHERE metric_name='{}';
    """.format(metric)
    return sql

# Starting with 99 companies and 96 metrics
NUM_COMPANIES = 94
NUM_METRICS = 96

companies_too_many_metrics = []
companies_too_few_metrics = []
compaines_perfect = []
metrics_too_few_companies = []
metrics_perfect = []

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

    # for company in NASDAQ_100:
    #     sql = check_company(company)
    #     cursor.execute(sql)
    #     rows = cursor.fetchall()

    #     if len(rows) > NUM_METRICS:
    #         print(f"ERROR: {company} has more than 96 rows. Deleting company from table")
    #         sql = delete_company(company)
    #         cursor.execute(sql)
    #         conn.commit()
    #         companies_too_many_metrics.append(company)
    #     elif len(rows) < NUM_METRICS:
    #         companies_too_few_metrics.append(company)
    #     else:
    #         compaines_perfect.append(company)
    
    # print("##### COMPANIES WITH TOO MANY METRICS - Removed from table #####")
    # print(companies_too_many_metrics)
    # print("##### COMPANIES WITH TOO FEW METRICS #####")
    # print(companies_too_few_metrics)
    # print("##### COMPANIES WITH PERFECT METRICS #####")
    # print(compaines_perfect)
    # print(f">>> REMAINING COMPANIES: {len(compaines_perfect) + len(companies_too_few_metrics)}<<<")
    
    for metric in ESG_METRICS:
        sql = check_metric(metric)
        cursor.execute(sql)
        rows = cursor.fetchall()

        print(f"{metric} - {len(rows)} companies")
        if len(rows) > NUM_COMPANIES:
            print(f"ERROR: Metric {metric} has too many companies") # Should not run
        elif len(rows) < NUM_COMPANIES:
            metrics_too_few_companies.append(metric)
        else:
            metrics_perfect.append(metric)
    
    print("##### METRICS WITH TOO FEW COMPANIES #####")
    print(metrics_too_few_companies)
    print("##### METRICS WITH PERFECT COMPANIES #####")
    print(metrics_perfect)

    # Commit the transaction, Close connection and return results
    conn.commit()
    cursor.close()
    conn.close()

except Exception as e:
    raise e
