from flask import Flask
from flask import request # <- added


app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/chessgame', methods=['GET', 'POST'])
def chessgame():
	return request.form['application/json']