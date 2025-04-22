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