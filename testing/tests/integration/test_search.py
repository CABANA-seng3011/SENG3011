def test_search_ticker(client):
    payload = {"query": "AAPL"}
    response = client.post("/searchTicker", json=payload)
    
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    
    assert isinstance(data, dict) or isinstance(data, list)
    assert data, "Empty response from /searchTicker"

def test_search_name(client):
    payload = {"query": "Apple"}
    response = client.post("/searchName", json=payload)
    
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    
    assert isinstance(data, dict) or isinstance(data, list)
    assert data, "Empty response from /searchName"
