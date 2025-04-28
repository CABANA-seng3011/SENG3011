import pytest
from unittest.mock import patch
from flask import Flask, jsonify
from datetime import datetime

########################################################################################################
# NEWS ROUTES
# THE FOLLOWING TESTS CHECK THE /NEWSSCRAPE and /NEWSSENTIMENT ROUTES
########################################################################################################

#########################################
########## News Scrape ###############
#########################################

def test_missing_company_name(client):
    """Test when no company name is provided."""
    response = client.get("/newsScrape")
    assert response.status_code == 400
    assert b"Invalid params, please specify a company name." in response.data

def test_invalid_company_name(client):
    """Test when the provided company name is not in NASDAQ_100."""
    response = client.get("/newsScrape?name=FakeCompany")
    assert response.status_code == 400
    assert b"Invalid company. Available companies" in response.data

@patch("index.query_company")
@patch("index.valid_nasdaq_company", return_value=True)
def test_no_events_found(mock_valid, mock_query, client):
    """Test when no events are returned for a valid company."""
    mock_query.return_value = []
    response = client.get("/newsScrape?name=Apple")
    assert response.status_code == 404
    assert b"No events found for company" in response.data

@patch("index.query_company")
@patch("index.valid_nasdaq_company", return_value=True)
def test_valid_news_response(mock_valid, mock_query, client):
    """Test valid flow with mocked event response."""
    mock_query.return_value = {"events": [{"mock": "article"}]}  # Minimal mock structure

    # Patch the final data formatting function
    with patch("index.create_adage_data_model_fin", return_value={"mocked": "data"}):
        response = client.get("/newsScrape?name=Apple")

        # Assertions
        assert response.status_code == 200
        assert response.is_json
        assert "mocked" in response.get_json()

@patch("index.query_company", side_effect=Exception("Simulated error"))
@patch("index.valid_nasdaq_company", return_value=True)
def test_company_news_exception(mock_valid, mock_query, client):
    """Test internal error handling for company news route."""
    response = client.get("/newsScrape?name=Apple")
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

    response = client.get("/newsScrape", query_string={
        "name": "Tesla Inc",
        "limit": "10",
        "start_date": "2025-04-17",
        "end_date": "2025-04-18"
    })

    assert response.status_code == 200
    assert response.get_json() == {"mocked": "result"}

#########################################
########## News Sentiment ###############
#########################################

def test_news_sentiment(client):
    payload = {"stockCode": "AAPL"}
    response = client.post("/newsSentiment", json=payload)
    
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    
    assert isinstance(data, dict)
    assert "stockCode" in data or "summary" in data
