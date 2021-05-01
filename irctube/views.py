from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename

from . import db

import os

# from symmetric_crypto import generate_password

from irctube.symmetric_crypto import generate_password


from irctube import app

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def index():

    return render_template("home.html")


@views.route("/profile")
def profile():
    return render_template("profile.html")


@views.route("/password_generator", methods=["GET", "POST"])
def password_generator():

    result = None
    if request.method == "POST":

        password_length = int(request.form["password_length"])
        character_set = request.form["password_complexity_dropdown"]
        result = generate_password(character_set, password_length)
    return render_template("password_generator.html", result=result)


@views.route("/single_key_methods", methods=["GET", "POST"])
def single_key_methods():

    return render_template("single_key.html", method=["GET", "POST"])


@views.route("/rsa_methods", methods=["GET", "POST"])
def rsa_methods():
    return render_template("rsa.html", methods=["GET", "POST"])


@app.route("/upload_success", methods=["GET", "POST"])
def get_file():

    if request.method == "POST":
        file_from_user = request.files["user_image_file"]
        filename = secure_filename(file_from_user.filename)
        file_from_user.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        text = request.form["message_to_encrypt_textbox"]
        processed_text = text.upper()

        return render_template("upload_success.html", filename=filename)
