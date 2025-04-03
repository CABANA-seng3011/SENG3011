import pytest
from unittest.mock import patch
from flask import Flask, jsonify
from index import app 

##########################################################################
# /GETCOMPANIES ROUTE
# THE FOLLOWING TESTS CHECK THE /GETCOMPANIES ROUTE
##########################################################################

@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("index.run_sql_raw")
def test_getCompanies_valid_industry(mock_run_sql, client):
    """Test the /getCompanies route with a valid industry."""
    # Simulate a successful SQL query
    mock_run_sql.return_value = [{"company_name": "PrimeCity Investment PLC"}]

    # Make a GET request to the /getCompanies route
    response = client.get(
        "/getCompanies?industry=Real+Estate"
    )

    # Assertions
    assert response.status_code == 200
    assert response.json == {"company_name": "PrimeCity Investment PLC"}

@patch("index.run_sql_raw")
def test_getCompanies_no_industry(client):
    """Test the /getCompanies route with no industry."""
    # Make a GET request to the /getCompanies route with no industry
    response = client.get(
        "/getCompanies"
    )
  
    assert response.status_code == 400
    assert response.data.decode() == "Invalid params, please specify an industry. See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/964329628/Available+Companies+and+Industries for allowed industries."
  
@patch("index.run_sql_raw")
def test_getCompanies_invalid_industry(mock_run_sql, client):
    """Test the /getCompanies route with an invalid industry."""
    # Simulate a successful SQL query
    mock_run_sql.return_value = []

    # Make a GET request to the /getCompanies route with an invalid industry
    response = client.get(
        "/getCompanies?industry=CABANA"
    )

    # Assertions
    assert response.status_code == 400
    assert response.data.decode() == "No companies found for 'CABANA'. See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/964329628/Available+Companies+and+Industries for allowed industries"

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