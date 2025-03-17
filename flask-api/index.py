from flask import Flask
import adage

app = Flask(__name__)

# Reachable through: curl http://127.0.0.1:5000/hello
@app.route('/hello')
def hello():
    return 'Hello, World!'

# Retrieve one or more matching ESG objects based on company name
@app.route('/get/<company_name>')
def get(company_name):
    return adage.getCompany(company_name)