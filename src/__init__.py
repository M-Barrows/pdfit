from flask import Flask, render_template, request, url_for, redirect
from src.libs import create_pdf
from logging.config import dictConfig

def create_app():
    dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
    
    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def home():
        return "Hi There",200

    @app.route("/create", methods=["GET","POST"])
    def create_doc(): 
        if request.method == "POST":
            urls = request.form.getlist("url")
            create_pdf(urls)
            return render_template("form-data.html",urls=request.form.getlist("url")),200
        else:
            return render_template("index.html"),200

    @app.route("/add-image", methods=["GET","POST"])
    def add_image():
        return "<div><input name='url' type='text'></div>",200

    return app

