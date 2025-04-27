import pytest
from unittest.mock import patch

########################################################################################################
# NASDAQ100 ROUTES
# THE FOLLOWING TESTS CHECK THE /SCORE AND /GET/NASDAQ ROUTE
########################################################################################################

########################################################################################################
# /GET/NASDAQ100 ROUTE
########################################################################################################

def test_get_nasdaq100_invalid_columns(client):
    """Test the /get/nasdaq100 route with invalid columns."""
    response = client.get("/get/nasdaq100?columns=invalid_column&company_name=Synopsys+Inc")

    assert response.status_code == 400
    assert response.data.decode() == (
        "Invalid columns. Columns should be a comma-separated String of valid columns. "
        "See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/961150999/Allowed+columns+for+get for valid columns."
    )

@patch("index.run_sql")
def test_get_nasdaq100_valid_columns(mock_run_sql, client):
    """Test the /get/nasdaq100 route with valid columns."""
    mock_run_sql.return_value = [
        {"company_name": "Synopsys Inc", "metric_name": "GOV_QUALITY", "metric_value": 88.5}
    ]

    response = client.get("/get/nasdaq100?columns=company_name,metric_name,metric_value&company_name=Synopsys+Inc")

    assert response.status_code == 200
    assert response.json.events[0].company_name == "Synopsys Inc"
    assert "dataset_id" in response.json

@patch("index.run_sql")
def test_get_nasdaq100_sql_exception(mock_run_sql, client):
    """Test the /get/nasdaq100 route when a SQL exception occurs."""
    mock_run_sql.side_effect = Exception("SQL Exception occurred.")

    response = client.get("/get/nasdaq100?columns=company_name,metric_name,metric_value&company_name=Synopsys+Inc")

    assert response.status_code == 500
    assert response.data.decode() == (
        "SQL Exception likely caused by invalid conditions. "
        "See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/960921696/get+and+slowget for instructions on how to use /get"
    )

import pytest
from unittest.mock import patch

########################################################################################################
# /SCORE ROUTE
########################################################################################################

def test_score_invalid_company(client):
    """Test the /score route with an invalid company."""
    response = client.get("/score?company=Invalid+Corp")

    assert response.status_code == 400
    assert "Invalid company" in response.data.decode()

def test_score_invalid_category(client):
    """Test the /score route with an invalid category."""
    response = client.get("/score?category=Invalid+Category")

    assert response.status_code == 400
    assert "Invalid category" in response.data.decode()

@patch("index.run_sql")
def test_score_valid_company_category(mock_run_sql, client):
    """Test the /score route with valid company and category."""
    mock_run_sql.return_value = [
        {"category": "Social Opportunity", "company_name": "Starbucks Corp", "score": 87.2}
    ]

    response = client.get("/score?company=Starbucks+Corp&category=Social+Opportunity")

    assert response.status_code == 200
    assert response.json.events[0].company_name == "Starbucks Corp"

@patch("index.run_sql")
def test_score_all_scores(mock_run_sql, client):
    """Test the /score route with no parameters (all scores)."""
    mock_run_sql.return_value = [
        {"category": "Environmental Risk", "company_name": "Apple Inc", "score": 92.0}
    ]

    response = client.get("/score")

    assert response.status_code == 200
    assert response.is_json
    assert "events" in response.json

@patch("index.run_sql")
def test_score_sql_exception(mock_run_sql, client):
    """Test the /score route when a SQL exception occurs."""
    mock_run_sql.side_effect = Exception("SQL error")

    response = client.get("/score?company=Apple+Inc")

    assert response.status_code == 500
    assert response.data.decode() == "SQL Exception."
