import pytest
from unittest.mock import patch
from flask import Flask, jsonify
from index import app # Import the Flask app from the index.py file

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
    assert response.data.decode() == "Hello, Flask! It's Byron Petselis"

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
