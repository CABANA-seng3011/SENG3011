from flask import Flask, request, jsonify
import json
import requests

# Testing /get
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
try:
    params = {
        "industry": "Real Estate"
    }
    response = requests.get('http://127.0.0.1:5000/getCompanies', params=params)
    data = response.json()
    print(json.dumps(data, indent=2))
except Exception as err:
    jsonify({'error': f'Error occurred: {err}'}), 500