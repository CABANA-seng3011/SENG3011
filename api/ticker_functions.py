from dotenv import load_dotenv, find_dotenv
import os
import requests
import json
import datetime

# Load the API Key for FMP
def get_key():
    load_dotenv(find_dotenv())
    return os.getenv("FMP_KEY")

# Retrieve information based on the ticker
def query_ticker(ticker):
    params = {
        "query": ticker,
        "apikey": get_key(),
    }

    try:
        response = requests.get(f"https://financialmodelingprep.com/stable/search-symbol", params=params)
        return response.json()
    
    except Exception as err:
        return err

# Retrive information based on the company name
def query_name(name):
    params = {
        "query": name,
        "apikey": get_key(),
    }

    try:
        response = requests.get(f"https://financialmodelingprep.com/stable/search-name", params=params)
        return response.json()

    except Exception as err:
        return err

def create_adage_data_model_fin(events):
    data_info = {
        "data_source": "Financial Modelling Prep",
        "dataset_type": "Financial Data covering 70,000+ stocks", 
        "dataset_id": "https://site.financialmodelingprep.com/",
        "time_object": { 
            "timestamp": str(datetime.datetime.now()), 
            "timezone": "GMT+11",
        },
        "events": events
    }
    return data_info