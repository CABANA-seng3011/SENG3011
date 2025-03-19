from db import run_sql
import re

# Creates an sql query based on the columns and parameters received
def create_sql_query(table, columns, conditions):
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
    return sql

def get_companies(industry):
    sql = """
    SELECT company FROM industry
    WHERE industry = '{}'
    """.format(industry)
    return sql

def valid_category(category):
    # Check if table is valid
    allowed_categories = ["esg", "environmental_opportunity", "environmental_risk", "governance_opportunity", 
                      "governance_risk", "social_opportunity", "social_risk"]
    if category.lower() not in allowed_categories:
        return False
    else:
        return True
        
def valid_columns(columns, category):
    columns_formatted = re.sub(' ', '', columns)
    columns_array = columns_formatted.split(',')
    # TODO: Write a list of allowed columns, raise exceptions where possible

# Tests:
# sql_runner (Create a really simple table to show that the connection works)
# get
# getIndustry