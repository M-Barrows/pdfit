from flask import Flask, render_template, request, url_for, redirect, send_from_directory,jsonify
from src.libs import create_pdf
from logging.config import dictConfig
import os
from src.db import db, Document, Image, doc_img_association
from sqlalchemy import func, desc

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
            doc_object, successful_images, failed_urls = create_pdf(urls)
            db.session.add(doc_object)
            db.session.commit()
            for img in successful_images:
                try:
                    img = db.session.query(Image).where(Image.image_url == img.image_url).one()
                except:
                    db.session.add(img)
                    db.session.commit()
                else:
                    img=img
                finally:
                    doc_object.images.append(img)
            db.session.flush()
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
        if request.method == "POST":
            print(request.args.get("link"))
            return render_template("add-image.html",link=request.args.get("link"))
        else: 
            return render_template("add-image.html"),200
        
    
    @app.route("/apps/pdfit/top-images/<int:n>", methods = ["GET"])
    def get_top_images(n:int):
        top_n_images = db.session.query(func.count(Document.id).label("usage_count"), Image.storage_location,Image.id,Image.image_url).select_from(Image).join(doc_img_association).join(Document).group_by(Image.id).limit(n).all()
        top_n_images = [img._asdict() for img in top_n_images]
        [img.update({"file_name":img.get("storage_location").split("/")[-1]}) for img in top_n_images]
        return render_template("top-images.html",top_n_images=top_n_images)

    @app.route("/apps/pdfit/image/<int:id>", methods = ["GET"])
    def get_image(id:int):
        img = db.get_or_404(Image,id)
        return f"<img class='card-img-top' src={img}>"
    
    @app.route("/apps/pdfit/image/<path:filename>", methods = ["GET"])
    def download_image(filename):
        print(filename)
        return send_from_directory("../files/image-library/",filename,as_attachment=True)

    return app
