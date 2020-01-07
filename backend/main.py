from flask import Flask, render_template

# from resource_validation import testwork

app = Flask(__name__)


@app.route('/')
def index():
	return render_template("index.html")

if __name__ == "__main__":
    app.config.from_object('configurations.DevelopmentConfig')
    app.run()