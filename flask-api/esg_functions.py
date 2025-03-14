from db import run_sql

# Find out how to turn /get?company_name=meow&metric_name=meow into an SQL query

# Creates an sql query based on the columns and parameters received
def create_sql_query(table, columns, params):
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
    conditions = []
    for k, v in params.items():
        conditions.append("{} = '{}'".format(k, v))
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    return sql


# Another parameter for sorting? limit?

# Implement /getIndustry

# Tests:
# sql_runner (Create a really simple table to show that the connection works)
# get
# getIndustry