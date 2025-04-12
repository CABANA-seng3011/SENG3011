from dotenv import load_dotenv, find_dotenv
from api.constants import NASDAQ_100, ESG_METRICS
import os
import psycopg2

def get_company_metrics(company, metric):
    sql = """
    SELECT company_name, perm_id, data_type, disclosure, metric_description, metric_name, metric_unit, metric_value, metric_year, nb_points_of_observations, metric_period, provider_name, reported_date, pillar, headquarter_country, category
    FROM esg_nasdaq_100
    WHERE company_name='{}'
    AND metric_name='{}'
    ORDER BY reported_date DESC; 
    """.format(company, metric)
    return sql

# Delete a row
def del_sql(row):
    if row[12] is None:
        reported_date = "AND reported_date IS NULL"
    else:
        reported_date = f"AND reported_date = \'{row[12]}\'"

    # AND reported_date IS NULL
    # AND reported_date = \'{row[12]}\'

    del_sql = f"""
    DELETE FROM esg_nasdaq_100
    WHERE company_name = \'{row[0]}\'
    AND perm_id = \'{row[1]}\'
    AND data_type = \'{row[2]}\'
    AND disclosure = \'{row[3]}\'
    AND metric_name = \'{row[5]}\'
    AND metric_unit = \'{row[6]}\'
    AND metric_value = \'{row[7]}\'
    AND nb_points_of_observations = \'{row[9]}\'
    AND provider_name = \'{row[11]}\'
    {reported_date}
    AND pillar = \'{row[13]}\'
    AND headquarter_country = \'{row[14]}\'
    AND category = \'{row[15]}\'
    """
    return del_sql

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

    for company in NASDAQ_100:
        print(f">>> Deleting rows for Company {company}...<<<")
        success = 0
        warning = 0
        warnings = []
        error = 0

        for metric in ESG_METRICS:
            # Check number of rows before delete
            sql = get_company_metrics(company, metric)
            cursor.execute(sql)
            rows = cursor.fetchall()
            start = len(rows)

            # One row
            if len(rows) == 1:
                success += 1
                continue

            # Delete rows and commit if there is more than 1 row
            if len(rows) > 1:
                for row in rows[1:]:
                    cursor.execute(del_sql(row))
                conn.commit()
            
            # Check numer of rows after delete
            sql = get_company_metrics(company, metric)
            cursor.execute(sql)
            rows = cursor.fetchall()
            after_delete = len(rows)
            
            # Check for 1 row leftover
            if after_delete == 1:
                # print(f"SUCCESS: Company {company} | Metric {metric}")
                success += 1
                
            if after_delete > 1:
                error += 1
                print(f"ERROR: Company {company} | Metric {metric} | Ended with {after_delete} rows!")
                for row in rows:
                    print(f"{row[0]} - {row[5]} - {row[7]} - {row[12]}")
            
            # Check for no rows left over
            if after_delete == 0 and start == 0:
                warning += 1
                warnings.append(metric)
            elif after_delete == 0:
                error += 1
                print(f"ERROR: Company {company} | Metric {metric} | Ended with 0 rows! Started with {start} rows.")

        # Check how many metrics each company has
        sql = f"""
        SELECT *
        FROM esg_nasdaq_100
        WHERE company_name='{company}';
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        print(f">>> Company {company} has {len(rows)} total rows <<<")
        print(f">>> The following metrics have 0 rows: {warnings} <<<")
        print(f">>> Company {company} finished with {success} successes, {warning} warnings and {error} errors <<<")
            
    # Close connection 
    cursor.close()
    conn.close()

except Exception as e:
    raise e