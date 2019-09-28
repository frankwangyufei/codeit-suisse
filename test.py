from flask import Flask
from flask import request # <- added


app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/chessgame', methods=['POST'])
def chessgame():
	data = request.json
	print(format(data))
	return data[0]