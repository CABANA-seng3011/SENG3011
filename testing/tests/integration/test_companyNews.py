import pytest
from unittest.mock import patch
from flask import Flask, jsonify
from index import app  # Adjust if your app is imported differently
from api.news_scraper import query_company

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

@patch("api.news_scraper.requests.get")
def test_query_company_exception(mock_get):
    """Test query_company handles exceptions and returns empty list."""
    mock_get.side_effect = Exception("Network error")

    result = query_company(
        company="Apple",
        api_key="fake-key",
        limit=5,
        start_date="2024-01-01",
        end_date="2024-12-31"
    )

    assert result == []

def mock_response(json_data):
    mock = Mock()
    mock.json.return_value = json_data
    return mock

@patch("api.news_scraper.requests.get")
def test_query_company_success(mock_get):
    # Mock input with 3 events
    mock_get.return_value = mock_response({
        "events": [
            {
                "time_object": {"timestamp": "2024-03-10T12:00:00Z"},
                "event_type": "NEWS",
                "attribute": {"headline": "Earlier Event"}
            },
            {
                "time_object": {"timestamp": "2025-03-10T12:00:00Z"},
                "event_type": "NEWS",
                "attribute": {"headline": "Latest Event"}
            },
            {
                "time_object": {"timestamp": "2023-03-10T12:00:00Z"},
                "event_type": "NEWS",
                "attribute": {"headline": "Oldest Event"}
            }
        ]
    })

    result = query_company(
        company="Apple",
        api_key="test-key",
        limit=2,
        start_date="2023-01-01",
        end_date="2025-12-31"
    )

    assert isinstance(result, dict)
    assert "events" in result
    assert len(result["events"]) == 2

    timestamps = [e["time_object"]["timestamp"] for e in result["events"]]
    # Check descending order
    assert timestamps == sorted(timestamps, reverse=True)