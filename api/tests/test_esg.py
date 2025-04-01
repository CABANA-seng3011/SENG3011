import json
import pytest

from esg_functions import (
    valid_category,
    valid_columns,
    create_sql_query,
    create_adage_data_model,
    ALLOWED_COLUMNS
)

# Test valid_category function
def test_valid_category():
    assert valid_category("environmental_risk") is True
    assert valid_category("invalid_category") is False

# Test valid_columns function
def test_valid_columns():
    valid_col = "company_name, metric_name"
    invalid_col = "company_name, unknown_column"
    
    assert valid_columns(valid_col) is True
    assert valid_columns(invalid_col) is False

# Test create_sql_query
def test_create_sql_query():
    table = "esg"
    columns = "company_name, metric_value"
    conditions = {"company_name": "Tervita Corp", "metric_name": "SOXEMISSIONS"}
    query = create_sql_query(table, columns, conditions)
    
    expected_query = "SELECT company_name, metric_value FROM esg WHERE company_name = 'Tervita Corp' AND metric_name = 'SOXEMISSIONS'"
    assert query == expected_query

# Test create_adage_data_model
def test_create_adage_data_model():
    events = [{"company_name": "Tervita", "metric_name": "SOXEMISSIONS", "metric_value": "100"}]
    result = create_adage_data_model(events)
    
    assert "data_source" in result
    assert "events" in result
    assert len(json.loads(result)["events"]) == 1