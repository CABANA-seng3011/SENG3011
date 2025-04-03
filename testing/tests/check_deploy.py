import json
import requests

class Style():
  BLUE = "\033[34m"
  RESET = "\033[0m"

def request_runner(path, params):
    try:
        response = requests.get(f"https://esg-hub-production.up.railway.app/{path}", params=params)
        print(response)
        data = response.json()
        print(f"Status Code: {response.status_code}")
        print(json.dumps(data, indent=2))
    
    except Exception as err:
        print(f"Error Response: {response.content}")

def pprint(str):
    print(f"{Style.BLUE}{str}{Style.RESET}")

def check_get():
    # Normal get
    pprint("Checking normal get, should retrieve SOXEMISSIONS for Tervita Corp...")
    normal_get_params = {
            "category": "environmental_risk",
            "columns": "company_name, metric_name, metric_value",
            # Conditions to limit to a specific company and metric:
            "company_name": "Tervita Corp",
            "metric_name": "SOXEMISSIONS"
    }
    request_runner("get", normal_get_params)

    # Invalid category
    pprint("Checking invalid category, should return 400 with error message...")
    invalid_category_get_params = {
            "category": "blahblahblah",
            "columns": "company_name, metric_name, metric_value",
            "company_name": "Tervita Corp",
            "metric_name": "SOXEMISSIONS"
    }
    request_runner("get", invalid_category_get_params)

    # Invalid columns
    pprint("Checking invalid columns, should return 400 with error message...")
    invalid_cols_get_params = {
            "category": "environmental_risk",
            "columns": "company_name, metric_name, metric_value, something_wrong",
            "company_name": "Tervita Corp",
            "metric_name": "SOXEMISSIONS"
    }
    request_runner("get", invalid_cols_get_params)

    # Invalid conditions
    pprint("Checking invalid conditions, should return 500 with error message...")
    invalid_conds_get_params = {
            "category": "environmental_risk",
            "columns": "company_name, metric_name, metric_value",
            "something_wrong": "Tervita Corp",
            "metric_name": "SOXEMISSIONS"
    }
    request_runner("get", invalid_conds_get_params)

def check_get_industry():
    # Normal get_industry
    pprint("Checking normal get industry, should retrieve 'Real Estate' for 'PrimeCity Investment PLC'...")
    normal_get_params = {
            "company": "PrimeCity Investment PLC"
    }
    request_runner("getIndustry", normal_get_params)

    # Invalid company
    pprint("Checking invalid company, should return 400 with error message...")
    invalid_industry_params = {
            "company": "Meow meow meow meow"
    }
    request_runner("getIndustry", invalid_industry_params)

    # No company (Invalid params)
    pprint("Checking invalid params, should return 400 with error message...")
    invalid_industry_params = {
            "invalid": "PrimeCity Investment PLC"
    }
    request_runner("getIndustry", invalid_industry_params)

def check_get_companies():
    # Normal get_companies
    pprint("Checking normal get companies, should retrieve a bunch of companies for 'Real Estate'...")
    normal_get_params = {
            "industry": "Real Estate"
    }
    request_runner("getCompanies", normal_get_params)

    # Invalid industry
    pprint("Checking invalid industry, should return 400 with error message...")
    invalid_industry_params = {
            "industry": "Meow meow meow meow"
    }
    request_runner("getCompanies", invalid_industry_params)

    # No industry, invalid params
    pprint("Checking invalid params, should return 400 with error message...")
    invalid_industry_params = {
            "invalid": "Real Estate"
    }
    request_runner("getCompanies", invalid_industry_params)


if __name__ == "__main__":
    check_get()
    check_get_industry()
    check_get_companies()
