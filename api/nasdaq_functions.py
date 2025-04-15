from esg_functions import create_sql_query
from constants import NASDAQ_100, CATEGORIES

def create_nasdaq_sql_query(columns, conditions):
    NASDAQ_TABLE = "esg_nasdaq_100"
    return create_sql_query(NASDAQ_TABLE, columns, conditions)

def get_all_scores():
    sql = """
    SELECT category, company_name, score
    FROM scores
    """
    return sql

def get_category_scores(category):
    sql = f"""
    SELECT category, company_name, score
    FROM scores
    WHERE category = '{category}'
    """
    return sql

def get_company_all_scores(company):
    sql = f"""
    SELECT category, company_name, score
    FROM scores
    WHERE company_name = '{company}'
    """
    return sql


def get_company_scores(company, category):
    sql = f"""
    SELECT category, company_name, score
    FROM scores
    WHERE company_name = '{company}'
    AND category = '{category}'
    """
    return sql

def valid_nasdaq_company(company):
    return company in NASDAQ_100

def valid_nasdaq_category(category):
    return category in CATEGORIES