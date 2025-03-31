from flask import Flask, request, jsonify, Response
from esg_functions import create_sql_query, get_industry, get_companies, valid_category, valid_columns, ALLOWED_COLUMNS, create_column_array, create_adage_data_model, create_companies_response
from db import run_sql, run_sql_raw

from flask_cors import CORS

# To run the app: flask --app index run
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Hello, Flask! It's Byron Petselis"

@app.route("/dummy")
def dummy():
    return "Hello, Flask! This is a dummy route for CD Testing"

# Reachable through: curl http://127.0.0.1:5000/hello
@app.route('/hello')
def hello():
    return 'Hello, World! Its CABANA'

# Example of use: 
# curl "http://127.0.0.1:5000/get?category=environmental_risk&columns=company_name,+metric_name,+metric_value&company_name=Tervita+Corp"
# Retrieves the columns: company_name, metric_name and metric value WHERE company_name is Tervita Corp
@app.route('/get', methods=['GET'])
def get():
    """
    Retrieves ESG information from an RDS instance.
    Faster than slow_get since ESG information is in separate tables based on the category.

    Args:
        category (String): One of the ESG pillars that correspond to a table in the database
        [optional] columns (String): A comma separating each column that the user wants to retrieve
            Eg, "company_name, metric_name, metric_value"
        [optional] conditions (String): 0 or more conditions to restrict your search
            Eg, "company_name=Tervita+Corp" OR "metric_value=SOXEMISSIONS"
    """
    # Separate parameters into category, column and conditions
    category = request.args.get("category")
    columns = request.args.get("columns")
    conditions = request.args.to_dict()

    # Check if category exists and is valid
    if category and not valid_category(category):
        res = "Invalid category. Allowed categories are: \"environmental_opportunity\", \"environmental_risk\", \"governance_opportunity\", \"governance_risk\", \"social_opportunity\", \"social_risk\""
        return Response (res, 400)
    else:
        conditions.pop("category")
    
    # If columns exist, check if valid
    if columns and not valid_columns(columns):
        res = "Invalid columns. Columns should be a comma-separated String of valid columns. See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/961150999/Allowed+columns+for+get for valid columns."
        return Response (res, 400)
    elif columns:
        conditions.pop("columns")
    # If no columns provided, select ALL columns
    else:
        columns = ",".join(ALLOWED_COLUMNS)
    
    sql = create_sql_query(category, columns, conditions)
    try:
        res = run_sql(sql, create_column_array(columns))
        return jsonify(create_adage_data_model(res))
    except Exception as e:
        res = "SQL Exception likely caused by invalid conditions. See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/960921696/get+and+slowget for instructions on how to use /get"
        return Response (res, 500)
    
@app.route('/slowget', methods=['GET'])
def slow_get():
    # Separate parameters into column and conditions
    columns = request.args.get("columns")
    conditions = request.args.to_dict()

    if columns and not valid_columns(columns):
        res = "Invalid columns. Columns should be a comma-separated String of valid columns. See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/961150999/Allowed+columns+for+get for valid columns."
        return Response (res, 400)
    elif columns:
        conditions.pop("columns")
    else:
        columns = ",".join(ALLOWED_COLUMNS)

    try:
        sql = create_sql_query("esg", columns, conditions)
        res = run_sql(sql, create_column_array(columns))
        return jsonify(create_adage_data_model(res))
    except Exception as e:
        res = "SQL Exception likely caused by invalid conditions. See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/960921696/get+and+slowget for instructions on how to use /get"
        return Response (res, 500)

# Example of use: curl "http://127.0.0.1:5000/getIndustry?company=PrimeCity+Investment+PLC"
@app.route('/getIndustry', methods=['GET'])
def getIndustry():
    company = request.args.get("company")
    
    try:
        res = run_sql(get_industry(company), ["industry"])
        if len(res) == 0:
            res = f"No industry found for '{company}'. See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/964329628/Available+Companies+and+Industries for allowed companies."
            return Response (res, 400)
        else:
            return jsonify(res)
    
    except Exception as e:
        res = "SQL Exception occurred."
        return Response (res, 500)
    
# Example of use: curl "http://127.0.0.1:5000/getCompanies?industry=Real+Estate"
@app.route('/getCompanies', methods=['GET'])
def getCompanies():
    industry = request.args.get("industry")
    try:
        rows = run_sql_raw(get_companies(industry))
        if len(rows) == 0:
            res = f"No companies found for '{industry}'. See https://unswcse.atlassian.net/wiki/spaces/SCAI/pages/964329628/Available+Companies+and+Industries for allowed industries"
            return Response (res, 400)
        else:
            res = create_companies_response(rows)
            return jsonify(res)
        
    except Exception as e:
        res = "SQL Exception occurred."
        return Response (res, 500)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)