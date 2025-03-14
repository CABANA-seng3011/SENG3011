from db import run_sql

# Creates an sql query based on the columns and parameters received
def create_sql_query(table, columns, conditions):
    # Check if table is valid
    allowed_tables = ["esg", "environmental_opportunity", "environmental_risk", "governance_opportunity", 
                      "governance_risk", "social_opportunity", "social_risk"]
    if table.lower() not in allowed_tables:
        raise Exception("Table {} does not exist. Check documentation for allowed tables", table)

    if columns is None:
        columns = "*"
    
    # Base query (SELECT, FROM)
    sql = "SELECT {} FROM {}".format(columns, table)

    # Conditions (WHERE, AND)
    conditions_sql = []
    for k, v in conditions.items():
        conditions_sql.append("{} = '{}'".format(k, v))
    if conditions_sql:
        sql += " WHERE " + " AND ".join(conditions_sql)
    return sql

def get_industry(company):
    sql = """
    SELECT industry FROM industry
    WHERE company = '{}'
    """.format(company)
    try:
        return run_sql(sql)
    except Exception as e:
        return e

def get_companies(industry):
    sql = """
    SELECT company FROM industry
    WHERE industry = '{}'
    """.format(industry)
    try:
        return run_sql(sql)
    except Exception as e:
        return e

# Implement /getIndustry

# Tests:
# sql_runner (Create a really simple table to show that the connection works)
# get
# getIndustry