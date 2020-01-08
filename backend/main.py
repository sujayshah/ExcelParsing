from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from resource_validation import testwork
from program_validation import ws
from tempfile import NamedTemporaryFile as ntf
from io import BytesIO as bio

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
    if fileStorage:
        # fileName = "new-excel.xlsx"
        # fileName = ntf()
        # fileStorage.save(fileName)

        # fileName = fileStorage.read()
        with ntf() as file:
            fileStorage.save(file)
            file.seek(0)
            testwork.openfile(file)
    return "resource"

if __name__ == "__main__":
    app.config.from_object('configurations.DevelopmentConfig')
    app.run()
