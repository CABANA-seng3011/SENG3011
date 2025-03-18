from flask import Flask, request, jsonify
from esg_functions import create_sql_query, get_industry, get_companies
from db import run_sql

# To run the app: flask --app index run
app = Flask(__name__)

# Reachable through: curl http://127.0.0.1:5000/hello
@app.route('/hello')
def hello():
    return 'Hello, World!'

# TODO: Error checking for all routes
@app.route('/get', methods=['GET'])
def get():
    # Separate parameters into category, column and conditions
    category = request.args.get("category")
    columns = request.args.get("columns")
    conditions = request.args.to_dict()
    conditions.pop("category")
    conditions.pop("columns")

    # TODO: Other possible parameters: limit, sort
    try:
        sql = create_sql_query(category, columns, conditions)
        res = run_sql(sql)
        return jsonify(res)
    except Exception as e:
        return jsonify(e) # TODO: Return a better exception object

@app.route('/getIndustry', methods=['GET'])
def getIndustry():
    company = request.args.get("company")
    try:
        res = run_sql(get_industry(company))
        return jsonify(res)
    except Exception as e:
        return jsonify(e)
    
# TODO: Fix data for the industry table, add escape characters to the & or replace with 'and'
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