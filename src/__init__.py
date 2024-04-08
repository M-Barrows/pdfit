from flask import Flask, render_template
from src.libs import create_pdf
def create_app():
    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def home():
        return "Hi There",200

    @app.route("/create", methods=["GET","POST"])
    def create_doc(): 
        # create_pdf() 
        return render_template("index.html"),200

    @app.route("/add-image", methods=["GET","POST"])
    def add_image():
        return "<div><input type='text'></div>",200

    return app

