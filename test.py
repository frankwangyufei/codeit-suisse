from flask import Flask
from flask import request # <- added


app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/chessgame', methods=['POST'])
def chessgame():
	data = request.get_json(force=True)
	print(format(data))
	return data