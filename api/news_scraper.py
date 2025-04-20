import requests

def query_company(company, api_key, limit, start_date, end_date):
    params = {
        "api_key": api_key,
        "limit": limit,
        "start_date": start_date,
        "end_date": end_date
    }

    try:
        response = requests.get(f"http://134.199.163.172/company/{company}", params=params)
        return response.json()
    
    except Exception as err:
        return []