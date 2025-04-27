import pytest
from unittest.mock import patch

########################################################################################################
# /FINACNES ROUTE
# THE FOLLOWING TESTS CHECK THE /FINANCES ROUTES
########################################################################################################

def test_finances_graph(client):
    payload = {"stockcode": "AAPL"}
    response = client.post("/financesGraph", json=payload)
    
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    
    assert isinstance(data, dict)
    assert "closingPriceHistory" in data

def test_finances_overview(client):
    response = client.get("/financesOverview/AAPL")
    
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    
    assert isinstance(data, dict)
    assert "overview" in data or len(data) > 0, "Missing 'overview' or empty response in /financesOverview"

def test_finances_historical(client):
    payload = {"ticker": "AAPL"}
    response = client.get("/financesHistorical/AAPL?start_date=2025-04-02&end_date=2025-04-15&interval=1d")
    
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    
    assert isinstance(data, dict)
    assert "historical" in data and "symbol" in data

def test_finances_price(client):
    payload = {"ticker": "AAPL"}
    response = client.get("/financesPrice/AAPL")
    
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    
    assert isinstance(data, dict)
    assert "price" in data or "currentPrice" in data, "Missing price fields in /financesPrice"

def test_finances_options(client):
    payload = {"ticker": "AAPL"}
    response = client.get("/financesOptions/AAPL")
    
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    
    assert isinstance(data, dict)
    assert "calls" in data
