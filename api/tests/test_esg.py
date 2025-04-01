import json

from esg_functions import (
    valid_category,
    valid_columns,
    create_sql_query,
    create_adage_data_model,
    create_companies_response,
    get_industry,
    get_companies,
    create_column_array
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

# Test create_sql_query function
def test_create_sql_query():
    table = "esg"
    columns = "company_name, metric_value"
    conditions = {"company_name": "Tervita Corp", "metric_name": "SOXEMISSIONS"}
    query = create_sql_query(table, columns, conditions)
    
    expected_query = "SELECT company_name, metric_value FROM esg WHERE company_name = 'Tervita Corp' AND metric_name = 'SOXEMISSIONS'"
    assert query == expected_query

# Test create_adage_data_model function
def test_create_adage_data_model():
    events = [{"company_name": "Tervita", "metric_name": "SOXEMISSIONS", "metric_value": "100"}]
    result = create_adage_data_model(events)
    
    assert "data_source" in result
    assert "events" in result
    assert len(json.loads(result)["events"]) == 1

# Test create_companies_response function
def test_create_companies_response():
    rows = [("Company A",), ("Company B",)]
    response = create_companies_response(rows)
    parsed_response = json.loads(response)
    
    assert "companies" in parsed_response
    assert parsed_response["companies"] == ["Company A", "Company B"]

# Test get_industry function
def test_get_industry():
    company = "Tervita Corp"
    query = get_industry(company)
    
    expected_query = "SELECT industry FROM industry\n    WHERE company = 'Tervita Corp'\n    "
    assert query.strip() == expected_query.strip()

# Test get_companies function
def test_get_companies():
    industry = "Energy"
    query = get_companies(industry)
    
    expected_query = "SELECT company FROM industry\n    WHERE industry = 'Energy'\n    "
    assert query.strip() == expected_query.strip()

# Test create_column_array function
def test_create_column_array():
    columns = "company_name, metric_name, metric_value"
    result = create_column_array(columns)
    
    assert result == ["company_name", "metric_name", "metric_value"]