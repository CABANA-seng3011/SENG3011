from flask import Flask, request, jsonify
import json
import requests

# Helper function to run tests
def run_test(name, func):
    print(f"Running {name}...")
    try:
        func()
        print(f"{name}: PASSED\n")
    except Exception as err:
        print(f"{name}: FAILED - {err}\n")

# Testing /get
def sanity_get():
    try:
        params = {
            "category": "environmental_risk",
            "columns": "company_name, metric_name, metric_value",
            # Conditions to limit to a specific company and metric:
            "company_name": "Tervita Corp",
            "metric_name": "SOXEMISSIONS"
        }
        response = requests.get('http://127.0.0.1:5000/get', params=params)
        data = response.json()
        print(json.dumps(data, indent=2))
    except Exception as err:
        jsonify({'error': f'Error occurred: {err}'}), 500

# Testing /getIndustry
def sanity_getIndustry():
    try:
        params = {
            "company": "PrimeCity Investment PLC"
        }
        response = requests.get('http://127.0.0.1:5000/getIndustry', params=params)
        data = response.json()
        print(json.dumps(data, indent=2))
    except Exception as err:
        jsonify({'error': f'Error occurred: {err}'}), 500

# Testing /getIndustry
def sanity_getIndustry2():
    try:
        params = {
            "industry": "Real Estate"
        }
        response = requests.get('http://127.0.0.1:5000/getCompanies', params=params)
        data = response.json()
        print(json.dumps(data, indent=2))
    except Exception as err:
        jsonify({'error': f'Error occurred: {err}'}), 500

# Additional tests
def test_get_valid():
    try:
        params = {
            "category": "environmental_risk",
            "columns": "company_name, metric_name, metric_value",
            "company_name": "Tervita Corp",
            "metric_name": "SOXEMISSIONS"
        }
        response = requests.get("http://127.0.0.1:5000/get", params=params)
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
    except Exception as err:
        print(f"Error in test_get_valid: {err}")

def test_get_invalid_category():
    try:
        params = {
            "category": "invalid_category",
            "columns": "company_name, metric_name, metric_value"
        }
        response = requests.get("http://127.0.0.1:5000/get", params=params)
        assert response.status_code == 200
        assert response.json() == "Error 400: Invalid category"
    except Exception as err:
        print(f"Error in test_get_invalid_category: {err}")

def test_get_invalid_columns():
    try:
        params = {"category": "environmental_risk", "columns": "invalid_column"}
        response = requests.get("http://127.0.0.1:5000/get", params=params)
        assert response.status_code == 200
        assert response.json() == "Error 400: Invalid columns"
    except Exception as err:
        print(f"Error in test_get_invalid_columns: {err}")

# need to fix -- this test will call the WHOLE table which is way to much data
# def test_get_no_columns():
#     try:
#         params = {"category": "environmental_risk"}
#         response = requests.get("http://127.0.0.1:5000/get", params=params)
#         assert response.status_code == 200
#         assert isinstance(response.json(), dict)
#     except Exception as err:
#         print(f"Error in test_get_no_columns: {err}")

def test_getIndustry_valid():
    try:
        params = {"company": "PrimeCity Investment PLC"}
        response = requests.get("http://127.0.0.1:5000/getIndustry", params=params)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    except Exception as err:
        print(f"Error in test_getIndustry_valid: {err}")

def test_getIndustry_invalid():
    try:
        params = {"company": "NonExistent Corp"}
        response = requests.get("http://127.0.0.1:5000/getIndustry", params=params)
        assert response.status_code == 200
        assert response.json() == []
    except Exception as err:
        print(f"Error in test_getIndustry_invalid: {err}")

def test_getCompanies_valid():
    try:
        params = {"industry": "Real Estate"}
        response = requests.get("http://127.0.0.1:5000/getCompanies", params=params)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    except Exception as err:
        print(f"Error in test_getCompanies_valid: {err}")

def test_getCompanies_invalid():
    try:
        params = {"industry": "NonExistent Industry"}
        response = requests.get("http://127.0.0.1:5000/getCompanies", params=params)
        assert response.status_code == 200
        assert response.json() == []
    except Exception as err:
        print(f"Error in test_getCompanies_invalid: {err}")

if __name__ == "__main__":
    test_functions = [
        test_get_valid,
        test_get_invalid_category,
        test_get_invalid_columns,
        # test_get_no_columns,
        test_getIndustry_valid,
        test_getIndustry_invalid,
        test_getCompanies_valid,
        test_getCompanies_invalid
    ]
    for test in test_functions:
        run_test(test.__name__, test)
    
    print("Sanity Checks: Validate the outputs")
    sanity_get()
    sanity_getIndustry()
    sanity_getIndustry2()