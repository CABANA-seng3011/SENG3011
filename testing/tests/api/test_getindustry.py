import pytest
from unittest.mock import patch
from flask import Flask, jsonify
from index import app 

##########################################################################
# /GETINDUSTRY ROUTE
# THE FOLLOWING TESTS CHECK THE /GETINDUSTRY ROUTE
##########################################################################

@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("index.run_sql")
def test_getIndustry_valid_company(mock_run_sql, client):
    """Test the /getIndustry route with a valid company."""
    # Simulate a successful SQL query
    mock_run_sql.return_value = [{"industry": "Real Estate"}]

    # Make a GET request to the /getIndustry route
    response = client.get(
        "/getIndustry?company=PrimeCity+Investment+PLC"
    )

    # Assertions
    assert response.status_code == 200
    assert response.json == {"industry": "Real Estate"}

def test_getIndustry_no_company(client):
    """Test the /getIndustry route with an invalid company."""
    # Make a GET request to the /getIndustry route with no company
    response = client.get(
        "/getIndustry"
    )

    # Assertions
    assert response.status_code == 400
    assert response.data.decode() == "Invalid params, please specify a company. See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/964329628/Available+Companies+and+Industries for allowed companies."

def test_getIndustry_invalid_company(client):
    """Test the /getIndustry route without providing a valid company."""
    # Make a GET request to the /getIndustry route with an invalid company
    response = client.get(
        "/getIndustry?company=CABANA"
    )

    # Assertions
    assert response.status_code == 500
    assert response.data.decode() == "No industry found for 'CABANA'. See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/964329628/Available+Companies+and+Industries for allowed companies."

def test_sql_exception(client):
    """Test the /getIndustry route when a SQL exception occurs."""
    # Simulate an exception in the run_sql function
    with patch("index.run_sql") as mock_run_sql:
        mock_run_sql.side_effect = Exception("SQL Exception occurred.")
        
        # Make a GET request to the /getIndustry route
        response = client.get(
            "/getIndustry?company=PrimeCity+Investment+PLC"
        )

        # Assertions
        assert response.status_code == 500
        assert response.data.decode() == "SQL Exception occurred."