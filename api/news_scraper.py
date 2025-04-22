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
    
def query_company_stock_data(stock_code, api_key):
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