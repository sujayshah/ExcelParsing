from flask import Flask, render_template, request, send_file, send_from_directory
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
    resp_code = None
    palette = []
    for color in request.form.values():
        if color not in palette:
            palette.append(color)
    fileStorage = request.files.get('name')
    with ntf() as file:
        if fileStorage:
            fileStorage.save(file)
            # file.seek(0)
            # testwork.openfile(file, palette)
            resp = send_file(file.name, as_attachment=True, attachment_filename=file.name, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            # resp = send_from_directory('', file.name, as_attachment=True, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            resp_code = 200
            resp.headers['Access-Control-Allow-Origin'] = "*"
        else:
            resp = {} 
            resp_code = 400

    # fileName = "new-excel.xlsx"
    # fileStorage.save(fileName)
    # resp = send_file(fileName, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    # resp = send_from_directory('', fileName, as_attachment=True, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    # resp_code = 200

    return resp, resp_code

if __name__ == "__main__":
    app.config.from_object('configurations.DevelopmentConfig')
    # app.config.from_object('configurations.ProductionConfig')
    app.run()
