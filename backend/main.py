from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from resource_validation import testwork
from program_validation import ws

app = Flask(__name__)
CORS(app)

@app.route('/')
# @cross_origin(origin='localhost')
def index():
	return render_template("index.html")

@app.route('/static/program', methods=['POST'])
# @cross_origin()
def program_validation(origin='localhost'):
    return "program"

@app.route('/static/resource', methods=['POST'])
# @cross_origin(origin='localhost')
def resource_validation():
    fileStorage = request.files.get('name')
    fileName = "new-excel.xlsx"
    fileStorage.save(fileName)
    testwork.openfile(fileName)
    return "resource"

if __name__ == "__main__":
    app.config.from_object('configurations.DevelopmentConfig')
    app.run()
