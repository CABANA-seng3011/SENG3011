from flask import Flask, request, jsonify
from esg_functions import create_sql_query, get_industry, get_companies, valid_category
from db import run_sql

# dummy commit 1

# To run the app: flask --app index run
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask! It's Byron Petselis"

# Reachable through: curl http://127.0.0.1:5000/hello
@app.route('/hello')
def hello():
    return 'Hello, World! Its CABANA'

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
        [optional] conditions (String): 
        
    """
    # Separate parameters into category, column and conditions
    category = request.args.get("category")
    columns = request.args.get("columns")
    conditions = request.args.to_dict()
    conditions.pop("category")
    conditions.pop("columns")

    if not valid_category(category):
        return jsonify("Error 400: Invalid category")

    # TODO: Other possible parameters: limit, sort
    try:
        sql = create_sql_query(category, columns, conditions)
        res = run_sql(sql)
        return jsonify(res)
    except Exception as e:
        return jsonify(e) # TODO: Return a better exception object
    # TODO: Make sure the return object is a nice json, probably need to add a function in db.py to parse the results from SQL
    
@app.route('/slowget', methods=['GET'])
def slow_get():
    # Separate parameters into category, column and conditions
    columns = request.args.get("columns")
    conditions = request.args.to_dict()
    conditions.pop("columns")

    # TODO: Other possible parameters: limit, sort
    try:
        sql = create_sql_query("esg", columns, conditions)
        res = run_sql(sql)
        return jsonify(res)
    except Exception as e:
        return jsonify(e) # TODO: Return a better exception object

# Example of use: curl "http://127.0.0.1:5000/getIndustry?company=PrimeCity+Investment+PLC"
@app.route('/getIndustry', methods=['GET'])
def getIndustry():
    company = request.args.get("company")
    try:
        res = run_sql(get_industry(company))
        return jsonify(res)
    except Exception as e:
        return jsonify(e)
    
# TODO: Fix data for the industry table, add escape characters to the & or replace with 'and'
# Example of use: curl "http://127.0.0.1:5000/getCompanies?industry=Real+Estate"
@app.route('/getCompanies', methods=['GET'])
def getCompanies():
    industry = request.args.get("industry")
    try:
        res = run_sql(get_companies(industry))
        return jsonify(res)
    except Exception as e:
        return jsonify(e)

if __name__ == "__main__":
    app.run(debug=True)