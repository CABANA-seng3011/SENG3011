from db import run_sql
import json
import re

# CONSTANTS #####################################
ALLOWED_CATEGORIES = ["esg", "environmental_opportunity", "environmental_risk", "governance_opportunity", 
                      "governance_risk", "social_opportunity", "social_risk"]

ALLOWED_COLUMNS = ["company_name", "perm_id", "data_type", "disclosure", "metric_description", "metric_name", "metric_unit",
                       "metric_value", "metric_year", "nb_points_of_observations", "metric_period", "provider_name", 
                       "reported_date", "pillar", "headquarter_country", "category"]
#################################################

# Creates an sql query based on the columns and parameters received
def create_sql_query(table, columns, conditions):    
    # Base query (SELECT, FROM)
    sql = "SELECT {} FROM {}".format(columns, table)

    # Conditions (WHERE, AND)
    conditions_sql = []
    for k, v in conditions.items():
        conditions_sql.append("{} = '{}'".format(k, v))
    if conditions_sql:
        sql += " WHERE " + " AND ".join(conditions_sql)
    return sql

def create_adage_data_model(events):
    data_info = {
        "data_source": "Eurofidai Clarity AI ESG data",
        "dataset_type": "Environmental, Social, and Governance (ESG) metrics for 70,000 companies", 
        "dataset_id": "db-esg-data.us-east-1.rds.amazonaws.com",
        "time_object": { 
            "timestamp": "2025-02-25 00:00:00.000000", 
            "timezone": "GMT+11",
            "info": "Data is current as of 25 Feb, 2025",
            "period_covered": "Q1 2016 - Q4 2024"
        },
        "events": events
    }
    return json.dumps(data_info)

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
    if category.lower() not in ALLOWED_CATEGORIES:
        return False
    else:
        return True
        
def valid_columns(columns):    
    for col in create_column_array(columns):
        if col.lower() not in ALLOWED_COLUMNS:
            return False
    return True

def create_column_array(columns):
    columns_formatted = re.sub(' ', '', columns)
    return columns_formatted.split(',')