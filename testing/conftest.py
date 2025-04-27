import pytest
from api import index  # Adjust this import

@pytest.fixture
def client():
    app = api(testing=True)  # Ensure app is configured for testing
    with app.test_client() as client:
        yield client