import pytest
from unittest.mock import patch

########################################################################################################
# /FINACNES ROUTE
# THE FOLLOWING TESTS CHECK THE /FINANCES ROUTES
########################################################################################################

def test_finances_graph(client):
    payload = {"ticker": "AAPL", "metric": "revenue"}
    response = client.post("/financesGraph", json=payload)
    
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    
    assert isinstance(data, dict)
    assert "graphData" in data, "Missing 'graphData' in /financesGraph response"

def test_finances_overview(client):
    payload = {"ticker": "AAPL"}
    response = client.post("/financesOverview", json=payload)
    
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    
    assert isinstance(data, dict)
    assert "overview" in data or len(data) > 0, "Missing 'overview' or empty response in /financesOverview"

def test_finances_historical(client):
    payload = {"ticker": "AAPL"}
    response = client.post("/financesHistorical", json=payload)
    
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    
    assert isinstance(data, dict)
    assert "historical" in data or "prices" in data, "Missing expected keys in /financesHistorical"

def test_finances_price(client):
    payload = {"ticker": "AAPL"}
    response = client.post("/financesPrice", json=payload)
    
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    
    assert isinstance(data, dict)
    assert "price" in data or "currentPrice" in data, "Missing price fields in /financesPrice"

def test_finances_options(client):
    payload = {"ticker": "AAPL"}
    response = client.post("/financesOptions", json=payload)
    
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    
    assert isinstance(data, dict)
    assert "options" in data or "chains" in data, "Missing options data in /financesOptions"
