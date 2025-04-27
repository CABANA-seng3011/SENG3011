def test_search_name(client):
    payload = {"query": "Apple"}
    response = client.post("/searchName", json=payload)
    
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    
    assert isinstance(data, dict) or isinstance(data, list)
    assert data, "Empty response from /searchName"

def test_score(client):
    payload = {"ticker": "AAPL"}
    response = client.post("/score", json=payload)
    
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    
    assert isinstance(data, dict)
    assert "score" in data, "Missing 'score' field in /score response"
