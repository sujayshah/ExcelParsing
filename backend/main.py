from flask import Flask, render_template, request, send_file
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
    fileStorage = request.files.get('name')
    with ntf() as file:
        if fileStorage:
        # fileName = "new-excel.xlsx"
        # fileName = ntf()
        # fileStorage.save(fileName)
            fileStorage.save(file)
            # file.seek(0)
            ws.openfile(file)
    return "program"

@app.route('/static/resource', methods=['POST'])
# @cross_origin(origin='localhost')
def resource_validation():
    resp = None
    palette = []
    for color in request.form.values():
        if color not in palette:
            palette.append(color)
    fileStorage = request.files.get('name')
    with ntf() as file:
        if fileStorage:
            # fileName = "new-excel.xlsx"
            # fileName = ntf()
            # fileStorage.save(fileName)
            fileStorage.save(file)
            file.seek(0)
            # testwork.openfile(file, palette)
            resp = send_file(file.name)
        else:
            resp = None 
    print(resp)
    return resp

if __name__ == "__main__":
    app.config.from_object('configurations.DevelopmentConfig')
    app.run()
