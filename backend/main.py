from flask import Flask, render_template, request, send_file, send_from_directory, redirect, url_for
from flask_cors import CORS, cross_origin
from resource_validation import testwork
from program_validation import ws
from datetime import date, timedelta, datetime
# from tempfile import NamedTemporaryFile as ntf

app = Flask(__name__)
CORS(app)

# app.config["APPLICATION_ROOT"] = "/static"

# @app.route('/static')
# @cross_origin()
# def reroute_static():
    # return render_template("../index.html")

@app.route('/')
@app.route('/static/')
@cross_origin()
def index():
	return render_template("index.html")

@app.route('/static/program', methods=['POST'])
@cross_origin()
def program_validation():
    # try:
    palette = []
    start = None
    end = None
    for key, value in request.form.items():
        if key == 'start':
            start = datetime.strptime(value, "%m-%d-%Y").date()
        elif key == 'end':
            end = datetime.strptime(value, "%m-%d-%Y").date()
        elif value not in palette:
            palette.append(value)
    print(palette, start, end)
    fileStorage = request.files.get('name')
    
    fileName = "output.xlsx"
    fileStorage.save('/tmp/' + fileName)
    # ws.openfile(file, palette, start, end)
    # resp = send_file(fileName, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    resp = send_from_directory('/tmp', fileName, as_attachment=True, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    resp_code = 200
    # except:
    #     print("something went wrong")

    return resp, resp_code

@app.route('/static/resource', methods=['POST'])
@cross_origin()
def resource_validation():
    palette = []
    for color in request.form.values():
        if color not in palette:
            palette.append(color)
    fileStorage = request.files.get('name')
    # with ntf() as file:
    #     if fileStorage:
    #         fileStorage.save(file)
    #         # file.seek(0)
    #         # testwork.openfile(file, palette)
    #         resp = send_file(file.name, as_attachment=True, attachment_filename=file.name, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    #         # resp = send_from_directory('', file.name, as_attachment=True, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    #         resp_code = 200
    #         resp.headers['Access-Control-Allow-Origin'] = "*"
    #     else:
    #         resp = {} 
    #         resp_code = 400

    fileName = "output.xlsx"
    fileStorage.save('/tmp/' + fileName)
    # testwork.openfile(file, palette)
    # resp = send_file(fileName, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    resp = send_from_directory('/tmp', fileName, as_attachment=True, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    resp_code = 200

    return resp, resp_code

if __name__ == "__main__":
    # app.config.from_object('configurations.DevelopmentConfig')
    # app.run(host='0.0.0.0', port=8080)

    app.config.from_object('configurations.ProductionConfig')
    app.run()
