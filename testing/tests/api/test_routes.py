import pytest
from unittest.mock import patch
from flask import Flask
from index import app  # Importing the app from your index.py file

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

# /get error checks
@patch("index.run_sql")  # Patch run_sql in the context of index.py where it's used
def test_get_route_invalid_columns(mock_run_sql, client):
    """Test the /get route with invalid columns."""
    # Make a GET request to the /get route with invalid columns
    response = client.get(
        "/get?category=environmental_risk&columns=invalid_column&company_name=Tervita+Corp"
    )

    # Assertions
    assert response.status_code == 400
    assert response.data.decode() == "Invalid columns. Columns should be a comma-separated String of valid columns. See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/961150999/Allowed+columns+for+get for valid columns."

@patch("index.run_sql")  # Patch run_sql in the context of index.py where it's used
def test_get_route_sql_exception(mock_run_sql, client):
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