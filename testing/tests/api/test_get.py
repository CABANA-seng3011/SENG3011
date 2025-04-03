import pytest
from unittest.mock import patch
from flask import Flask, jsonify
from index import app 

##########################################################################
# /GET ROUTE
# THE FOLLOWING TESTS CHECK THE /GET ROUTE
##########################################################################

@patch("index.run_sql")  # Patch run_sql in the context of index.py where it's used
def test_get_invalid_columns(mock_run_sql, client):
    """Test the /get route with invalid columns."""

    response = client.get(
        "/get?category=environmental_risk&columns=invalid_column&company_name=Tervita+Corp"
    )

    # Assertions
    assert response.status_code == 400
    assert response.data.decode() == "Invalid columns. Columns should be a comma-separated String of valid columns. See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/961150999/Allowed+columns+for+get for valid columns."

@patch("index.run_sql")
def test_get_sql_exception(mock_run_sql, client):
    """Test the /get route when a SQL exception occurs."""
    # Simulate an exception in the run_sql function
    mock_run_sql.side_effect = Exception("SQL Exception occurred.")

    # Make a GET request to the /get route
    response = client.get(
        "/get?category=environmental_risk&columns=company_name,metric_name,metric_value&company_name=Tervita+Corp"
    )

    # Assertions
    assert response.status_code == 500
    assert response.data.decode() == "SQL Exception likely caused by invalid conditions. See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/960921696/get+and+slowget for instructions on how to use /get"

@patch("index.run_sql")
# Test the route if not proivded with ESG risk or opp
def test_get_invalid_category(mock_run_sql, client):
    """Test the /get route with an invalid category."""
    # Make a GET request to the /get route with an invalid category
    response = client.get(
        "/get?category=invalid_category&columns=company_name,metric_name,metric_value&company_name=Tervita+Corp"
    )

    # Assertions
    assert response.status_code == 400
    assert response.data.decode() == "Invalid category. Allowed categories are: \"environmental_opportunity\", \"environmental_risk\", \"governance_opportunity\", \"governance_risk\", \"social_opportunity\", \"social_risk\""

@patch("index.run_sql")
# Check if several columns are selected, are they joined
def test_get_valid_columns(mock_run_sql, client):
    """Test the /get route with valid columns."""
    # Simulate a successful SQL query
    mock_run_sql.return_value = [
        {"company_name": "Tervita Corp", "metric_name": "SOXEMISSIONS", "metric_value": 100}
    ]

    # Make a GET request to the /get route with valid columns
    response = client.get(
        "/get?category=environmental_risk&columns=company_name,metric_name,metric_value&company_name=Tervita+Corp"
    )

    # Assertions
    assert response.status_code == 200
    assert response.json == '{"data_source": "Eurofidai Clarity AI ESG data", "dataset_type": "Environmental, Social, and Governance (ESG) metrics for 70,000 companies", "dataset_id": "db-esg-data.us-east-1.rds.amazonaws.com", "time_object": {"timestamp": "2025-02-25 00:00:00.000000", "timezone": "GMT+11", "info": "Data is current as of 25 Feb, 2025", "period_covered": "Q1 2016 - Q4 2024"}, "events": [{"company_name": "Tervita Corp", "metric_name": "SOXEMISSIONS", "metric_value": 100}]}'
