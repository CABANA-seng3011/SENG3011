from flask import Flask, request, jsonify
from esg_functions import create_sql_query
from db import run_sql

# To run the app: flask --app index run
app = Flask(__name__)

# Reachable through: curl http://127.0.0.1:5000/hello
@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/get', methods=['GET'])
def get():
    params = request.args
    try:
        sql = create_sql_query("environmental_opportuniity", "company_name, metric_name, metric_value", params)
        res = run_sql(sql)
    except Exception as e:
        return jsonify(e) # TODO: Return a better exception object

    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True)