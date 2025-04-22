import requests
from dateutil import parser

def query_company(company, api_key, limit, start_date, end_date):
    params = {
        "api_key": api_key,
        "limit": limit,
        "start_date": start_date,
        "end_date": end_date
    }

    try:
        response = requests.get(f"http://134.199.163.172/company/{company}", params=params)

        data = response.json()

        if "events" in data:
            data["events"] = sorted(
                data["events"],
                key=lambda e: parser.parse(e["time_object"]["timestamp"]),
                reverse=True
            )[:int(limit)]

        return data
    
    except Exception as err:
        print(f"Error: {err}")
        return []
    
def query_company_sentiment(stock_code, api_key):
    url = "http://api-financeprodlb-421072170.ap-southeast-2.elb.amazonaws.com/analysis"
    payload = {
        "stockCode": stock_code,
        "apiKey": api_key
    }

    try:
        response = requests.post(url, json=payload)
        return response.json() if response.status_code == 200 else {"error": response.text}
    except Exception as e:
        return {"error": str(e)}
    
def query_finances_stock_data(stock_code, api_key):
    url = "http://api-financeprodlb-421072170.ap-southeast-2.elb.amazonaws.com/graph"
    payload = {
        "stockCode": stock_code,
        "apiKey": api_key
    }

    try:
        response = requests.post(url, json=payload)
        return response.json() if response.status_code == 200 else {"error": response.text}
    except Exception as e:
        return {"error": str(e)}
    
def query_finances_overview(symbol):
    url = f"https://8a38hm2y70.execute-api.ap-southeast-2.amazonaws.com/v1/stocks/overview/{symbol}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}
    except Exception as e:
        return {"error": str(e)}

def query_finances_price(symbol):
    url = f"https://8a38hm2y70.execute-api.ap-southeast-2.amazonaws.com/v1/stocks/price/{symbol}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}
    except Exception as e:
        return {"error": str(e)}
    
def query_finances_historical_data(symbol, start_date, end_date, interval):
    url = f"https://8a38hm2y70.execute-api.ap-southeast-2.amazonaws.com/v1/stocks/historical/{symbol}"
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "interval": interval
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}
    except Exception as e:
        return {"error": str(e)}
    
def query_finances_options_data(symbol):
    url = f"https://8a38hm2y70.execute-api.ap-southeast-2.amazonaws.com/v1/stocks/options/{symbol}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}
    except Exception as e:
        return {"error": str(e)}