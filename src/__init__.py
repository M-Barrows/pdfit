from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from src.libs import create_pdf
from logging.config import dictConfig
import os
from src.db import db, Document, Image, doc_img_association

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
    
    app = Flask(__name__, static_folder= 'static')
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/mab/database/pdfit.db"

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def health():
        return "Healthy",200

    @app.route("/apps/pdfit", methods=["GET"])
    def home():
        return "Hi There",200

    @app.route("/apps/pdfit/create", methods=["GET","POST"])
    def create_doc():
        if request.method == "POST":
            urls = request.form.getlist("url")
            doc_object, failed_urls = create_pdf(urls) 
            db.session.add(doc_object)
            db.session.commit()
            return render_template(
                "form-data.html",
                pdf_download_link=doc_object.name, 
                failed_urls=failed_urls,
                successful_urls=[image.image_url for image in doc_object.images]
            ),200
        else:
            return render_template("index.html"),200

    @app.route("/apps/pdfit/download/<path:filename>", methods = ["GET"])
    def download_pdf(filename):
        print(os.getcwd())
        return send_from_directory("../files/output",filename,as_attachment=True)
    
    @app.route("/apps/pdfit/add-image", methods=["GET","POST"])
    def add_image():
        return render_template("add-image.html"),200
    
    return app

