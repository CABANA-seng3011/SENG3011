import pytest
from unittest.mock import patch
from flask import Flask, jsonify
from index import app  # Adjust if your app is imported differently
from datetime import datetime

@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_missing_company_name(client):
    """Test when no company name is provided."""
    response = client.get("/companyNews")
    assert response.status_code == 400
    assert b"Invalid params, please specify a company name." in response.data

def test_invalid_company_name(client):
    """Test when the provided company name is not in NASDAQ_100."""
    response = client.get("/companyNews?name=FakeCompany")
    assert response.status_code == 400
    assert b"Invalid company. Available companies" in response.data

@patch("index.query_company")
@patch("index.valid_nasdaq_company", return_value=True)
def test_no_events_found(mock_valid, mock_query, client):
    """Test when no events are returned for a valid company."""
    mock_query.return_value = []
    response = client.get("/companyNews?name=Apple")
    assert response.status_code == 404
    assert b"No events found for company" in response.data

@patch("index.query_company")
@patch("index.valid_nasdaq_company", return_value=True)
def test_valid_news_response(mock_valid, mock_query, client):
    """Test valid flow with mocked event response."""
    mock_query.return_value = {"events": [{"mock": "article"}]}  # Minimal mock structure

    # Patch the final data formatting function
    with patch("index.create_adage_data_model_fin", return_value={"mocked": "data"}):
        response = client.get("/companyNews?name=Apple")

        # Assertions
        assert response.status_code == 200
        assert response.is_json
        assert "mocked" in response.get_json()

@patch("index.query_company", side_effect=Exception("Simulated error"))
@patch("index.valid_nasdaq_company", return_value=True)
def test_company_news_exception(mock_valid, mock_query, client):
    """Test internal error handling for company news route."""
    response = client.get("/companyNews?name=Apple")
    assert response.status_code == 500
    assert b"An Exception occurred." in response.data

@patch("index.valid_nasdaq_company", return_value=True)
@patch("index.query_company")
@patch("index.create_adage_data_model_fin")
def test_company_news_success(mock_create_model, mock_query_company, mock_valid_company, client):
    # Mock the query_company return value
    mock_query_company.return_value = {
        "events": [{"event_type": "News", "time_object": {"timestamp": "2025-04-18T15:00:00Z"}}]
    }

    # Mock the final output formatting
    mock_create_model.return_value = {"mocked": "result"}

    response = client.get("/companyNews", query_string={
        "name": "Tesla Inc",
        "limit": "10",
        "start_date": "2025-04-17",
        "end_date": "2025-04-18"
    })

    assert response.status_code == 200
    assert response.get_json() == {"mocked": "result"}

@patch("index.valid_nasdaq_company", return_value=True)
@patch("index.query_company")
@patch("index.create_adage_data_model_fin")
def test_company_news_events_sorted_desc(mock_create_model, mock_query_company, mock_valid_company, client):
    # Create out-of-order timestamps
    timestamps = [
        "2025-04-18T10:00:00Z",
        "2025-04-18T15:00:00Z",
        "2025-04-18T12:00:00Z",
    ]
    
    # Corresponding events
    events = [
        {"time_object": {"timestamp": ts}} for ts in timestamps
    ]

    # Mock query_company to return them unsorted
    mock_query_company.return_value = {"events": events}

    # Mock create_adage_data_model_fin to just return the events back
    def passthrough(events_data):
        return events_data
    
    mock_create_model.side_effect = passthrough

    response = client.get("/companyNews", query_string={
        "name": "Tesla Inc",
        "limit": "10",
        "start_date": "2025-04-17",
        "end_date": "2025-04-18"
    })

    assert response.status_code == 200
    sorted_events = response.get_json()["events"]

    # Extract timestamps from the response
    returned_timestamps = [
        e["time_object"]["timestamp"] for e in sorted_events
    ]

    # Parse them into datetime objects for comparison
    parsed = [datetime.fromisoformat(ts.replace("Z", "+00:00")) for ts in returned_timestamps]
    
    # Assert they are in descending order
    assert parsed == sorted(parsed, reverse=True)