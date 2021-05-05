from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    Response,
    send_file,
    session,
)
from flask_login import LoginManager, current_user

from flask_login.utils import login_required

from . import db
from irctube.models import FileContents
from irctube.symmetric_crypto import generate_password, generate_key

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

import io

encryption = Blueprint("encryption", __name__)


@encryption.route("/password_generator", methods=["GET", "POST"])
def password_generator():

    result = None
    if request.method == "POST":

        password_length = int(request.form["password_length"])
        character_set = request.form["password_complexity_dropdown"]
        result = generate_password(character_set, password_length)
    return render_template("password_generator.html", result=result)


@encryption.route("/single_key_methods/key_generator", methods=["GET", "POST"])
@login_required
def single_key_generator():

    key = None
    if request.method == "POST":
        key = generate_key(request.form["key_generator_textbox"])

        si = io.BytesIO()
        si.write(key)
        si.seek(0)

        uploaded_file = FileContents(
            user_id=current_user.id,
            name=request.form["file_name"],
            filetype="Single Key File",
            data=si.read(),
        )
        db.session.add(uploaded_file)
        db.session.commit()

        return send_file(
            si,
            as_attachment=True,
            attachment_filename="symmetric_secret.key",
            mimetype="text/plain",
        )

    return render_template("single_key/single_key_generator.html")


@encryption.route("/single_key_methods/file_encryption", methods=["GET", "POST"])
def single_key_file_encryption():

    if request.method == "POST":

        key = generate_key(request.form["key_encryption_password"])

        file_data = request.files["user_file_to_encrypt_single_key"].read()

        # make Fernet object that will encrypt file
        f = Fernet(key)
        encrypted_data = f.encrypt(file_data)

        # store encrypted data
        file_for_storage = io.BytesIO(encrypted_data)
        file_for_storage.seek(0)

        # upload encrypted data to database
        upload_encrypted_file = FileContents(
            user_id=current_user.id,
            name=request.form["file_name"],
            filetype="Single Key Encrypted File",
            data=file_for_storage.read(),
        )
        db.session.add(upload_encrypted_file)
        db.session.commit()

        key_file = io.BytesIO()
        key_file.write(key)
        key_file.seek(0)

        upload_key_file = FileContents(
            user_id=current_user.id,
            name=request.form["file_name"],
            filetype="Single Key File",
            data=key_file.read(),
        )
        db.session.add(upload_key_file)
        db.session.commit()

        return send_file(
            key_file,
            as_attachment=True,
            attachment_filename="symmetric_secret.key",
            mimetype="text/plain",
        )

    return render_template("single_key/file_encryption.html")


@encryption.route("/single_key_methods/file_decryption", methods=["GET", "POST"])
def single_key_file_decryption():

    if request.method == "POST":
        key_file = request.files["single_key_file"].read()
        encrypted_file = request.files["user_file_to_encrypt_single_key"].read()
    return render_template("single_key/file_decryption.html")


@encryption.route("/rsa/file_encryption", methods=["GET", "POST"])
def rsa_file_encryption():
    return render_template("rsa/file_encryption.html")


@encryption.route("/rsa/file_decryption", methods=["GET", "POST"])
def rsa_file_decryption():
    return render_template("rsa/file_decryption.html")
