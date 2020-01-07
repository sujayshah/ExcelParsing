from flask import Flask, render_template
from resource_validation import testwork
from program_validation import ws

from program_validation import ws
from resource_validation import testwork

app = Flask(__name__)

LOCAL_URL = 'localhost:5000'
PRODUCTION_URL = 'https://excel-parsing-258004.appspot.com'

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/static/program', methods=['POST'])
def program_validation():
    return("program")

@app.route('/static/resource', methods=['POST'])
def resource_validation():
    return("resource")

if __name__ == "__main__":
    app.config.from_object('configurations.DevelopmentConfig')
    app.run()
