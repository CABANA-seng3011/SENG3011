from flask import Flask

app = Flask(__name__)

# Reachable through: curl http://127.0.0.1:5000/hello
@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route("/")
def home():
    return "Hello, Flask is running!"

# dummy commit 11