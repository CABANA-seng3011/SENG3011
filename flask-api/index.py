from flask import Flask, request, jsonify
from esg_functions import create_sql_query, get_industry, get_companies, valid_category, valid_columns, ALLOWED_COLUMNS, create_column_array
from db import run_sql
from finance_functions import get_stock_price

# To run the app: flask --app index run
app = Flask(__name__)

# Reachable through: curl http://127.0.0.1:5000/hello
@app.route('/hello')
def hello():
    return 'Hello, World!'

# TODO: Error checking for all routes
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

    if not valid_category(category):
        return jsonify("Error 400: Invalid category")
    else:
        conditions.pop("category")
    
    if columns and not valid_columns(columns):
        return jsonify("Error 400: Invalid columns")
    elif columns:
        conditions.pop("columns")
    else:
        columns = ",".join(ALLOWED_COLUMNS)
    
    # TODO: Other possible parameters: limit, sort
    try:
        if columns:
            sql = create_sql_query(category, columns, conditions)
            res = run_sql(sql, create_column_array(columns))
        return jsonify(res)
    except Exception as e:
        print(e)
        return jsonify(e) # TODO: Return a better exception object for all routes
    # TODO: Make sure the return object is a nice json, probably need to add a function in db.py to parse the results from SQL
    
@app.route('/slowget', methods=['GET'])
def slow_get():
    # Separate parameters into column and conditions
    columns = request.args.get("columns")
    conditions = request.args.to_dict()

    if columns and not valid_columns(columns):
        return jsonify("Error 400: Invalid columns")
    elif columns:
        conditions.pop("columns")
    else:
        columns = ",".join(ALLOWED_COLUMNS)

    try:
        sql = create_sql_query("esg", columns, conditions)
        res = run_sql(sql, create_column_array(columns))
        return jsonify(res)
    except Exception as e:
        return jsonify(e)

# Example of use: curl "http://127.0.0.1:5000/getIndustry?company=PrimeCity+Investment+PLC"
@app.route('/getIndustry', methods=['GET'])
def getIndustry():
    company = request.args.get("company")
    try:
        res = run_sql(get_industry(company), ["industry"])
        return jsonify(res)
    except Exception as e:
        return jsonify(e)
    
# TODO: Fix data for the industry table, add escape characters to the & or replace with 'and'
# Example of use: curl "http://127.0.0.1:5000/getCompanies?industry=Real+Estate"
@app.route('/getCompanies', methods=['GET'])
def getCompanies():
    industry = request.args.get("industry")
    try:
        res = run_sql(get_companies(industry), ["company"])
        return jsonify(res)
    except Exception as e:
        return jsonify(e)

@app.route('/finance/stock-price', methods=['GET'])
def getStockPrices():
    company = request.args.get('company')
    if not company:
        return jsonify({"error": "No company name provided. Must include a company name as parameter"}), 400
    
    res = get_stock_price(company)
    if "error" in res:
        return jsonify(res), 500
    else:
        return jsonify(res), 200


if __name__ == "__main__":
    app.run(debug=True)