import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from index import app

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
    assert response.data.decode() == "Hello, Flask! It's me"

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

@patch("index.run_sql")
def test_get_route(mock_run_sql, client):
    """Test the /get route with mocked database interaction."""
    # Mock the database response
    mock_run_sql.return_value = [
        {"company_name": "Tervita Corp", "metric_name": "SOXEMISSIONS", "metric_value": "100"}
    ]

    # Make a GET request to the /get route
    response = client.get(
        "/get?category=environmental_risk&columns=company_name,metric_name,metric_value&company_name=Tervita+Corp"
    )

    # Assertions
    assert response.status_code == 200
    data = response.get_json()
    assert data == [
        {"company_name": "Tervita Corp", "metric_name": "SOXEMISSIONS", "metric_value": "100"}
    ]

    # Ensure the mocked function was called with the correct SQL query
    mock_run_sql.assert_called_once_with(
        "SELECT company_name, metric_name, metric_value FROM environmental_risk WHERE company_name = 'Tervita Corp'",
        ["company_name", "metric_name", "metric_value"]
    )