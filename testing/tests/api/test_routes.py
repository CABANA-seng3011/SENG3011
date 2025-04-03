import pytest
from unittest.mock import patch
from flask import Flask, jsonify
from index import app # Import the Flask app from the index.py file

@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    """Test the home route."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode() == "Hello, Flask! It's Byron Petselis"

def test_dummy_route(client):
    """Test the dummy route."""
    response = client.get("/dummy")
    assert response.status_code == 200
    assert response.data.decode() == "Hello, Flask! This is a dummy route for CD Testing"

def test_hello_route(client):
    """Test the hello route."""
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.data.decode() == "Hello, World! Its CABANA"

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
    assert response.json == '{"data_source": "Eurofidai Clarity AI ESG data", "dataset_type": "Environmental, Social, and Governance (ESG) metrics...Q1 2016 - Q4 2024"}, "events": [{"company_name": "Tervita Corp", "metric_name": "SOXEMISSIONS", "metric_value": 100}]}'

##########################################################################
# /SLOWGET ROUTE
# THE FOLLOWING TESTS CHECK THE /SLOWGET ROUTE
##########################################################################

@patch("index.run_sql")
def test_slowget_invalid_columns(mock_run_sql, client):
    """Test the /slowget route with invalid columns."""
    response = client.get(
        "/slowget?columns=invalid_column&company_name=Tervita+Corp"
    )

    # Assertions
    assert response.status_code == 400
    assert response.data.decode() == "Invalid columns. Columns should be a comma-separated String of valid columns. See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/961150999/Allowed+columns+for+get for valid columns."

@patch("index.run_sql")
def test_slowget_sql_exception(mock_run_sql, client):
    """Test the /slowget route when a SQL exception occurs."""
    # Simulate an exception in the run_sql function
    mock_run_sql.side_effect = Exception("SQL Exception occurred.")
    # Make a GET request to the /slowget route
    response = client.get(
        "/slowget?columns=company_name,metric_name,metric_value&company_name=Tervita+Corp"
    )
    assert response.status_code == 500
    assert response.data.decode() == "SQL Exception likely caused by invalid conditions. See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/960921696/get+and+slowget for instructions on how to use /get"

# Test the route if not proivded with ESG risk or opp
@patch("index.run_sql")
def test_slowget_invalid_category(mock_run_sql, client):
    """Test the /slowget route with an invalid category."""
    # Make a GET request to the /slowget route with an invalid category
    response = client.get(
        "/slowget?category=invalid_category&columns=company_name,metric_name,metric_value&company_name=Tervita+Corp"
    )

    # Assertions
    assert response.status_code == 500

# Check if several columns are selected, are they joined
@patch("index.run_sql")
def test_slowget_valid_columns(mock_run_sql, client):
    """Test the /slowget route with valid columns."""
    # Simulate a successful SQL query
    mock_run_sql.return_value = [
        {"company_name": "Tervita Corp", "metric_name": "SOXEMISSIONS", "metric_value": 100}
    ]

    # Make a GET request to the /slowget route with valid columns
    response = client.get(
        "/slowget?columns=company_name,metric_name,metric_value&company_name=Tervita+Corp"
    )

    # Assertions
    assert response.status_code == 200
    assert response.json == '{"data_source": "Eurofidai Clarity AI ESG data", "dataset_type": "Environmental, Social, and Governance (ESG) metrics...Q1 2016 - Q4 2024"}, "events": [{"company_name": "Tervita Corp", "metric_name": "SOXEMISSIONS", "metric_value": 100}]}'