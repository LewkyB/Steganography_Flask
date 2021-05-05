from flask import (
    Blueprint,
    render_template,
    request,
    send_file,
)
from flask_login import current_user

from flask_login.utils import login_required
import base64

from . import db
from encryption_tools.models import FileContents
from encryption_tools.symmetric_crypto import (
    generate_password,
    generate_key,
)

from cryptography.fernet import Fernet

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

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

        # upload key to database
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

    # store all of available single key files for display on html template
    user_files = FileContents.query.filter_by(
        user_id=current_user.id, filetype="Single Key Encrypted File"
    ).all()

    print(user_files)

    if request.method == "POST":
        key_file = request.files["single_key_file"].read()
        encrypted_file = request.files["user_file_to_decrypt_single_key"].read()

        f = Fernet(key_file)
        decrypted_data = f.decrypt(encrypted_file)

        decrypted_file = io.BytesIO()
        decrypted_file.write(decrypted_data)
        decrypted_file.seek(0)

        return send_file(
            decrypted_file,
            as_attachment=True,
            attachment_filename="decrypted_file",
            mimetype="text/plain",
        )

    return render_template("single_key/file_decryption.html", user_files=user_files)


@encryption.route("/rsa/file_encryption", methods=["GET", "POST"])
def rsa_file_encryption():

    if request.method == "POST":

        # create private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        # convert password to bytes for use with serialization
        byte_pass = bytes(request.form["rsa_key_password"], "utf-8")

        # create private key with password
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(byte_pass),
        )

        # prepare public key
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        # load and encrypt data
        file_data = request.files["user_file_to_encrypt_rsa"].read()
        encrypted_data = public_key.encrypt(
            file_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        b64_encrypted_data = base64.urlsafe_b64encode(encrypted_data)

        file_for_storage = io.BytesIO(b64_encrypted_data)
        file_for_storage.seek(0)

        # upload encrypted data to database
        upload_encrypted_file = FileContents(
            user_id=current_user.id,
            name=request.form["file_name"],
            filetype="RSA Encrypted File",
            data=file_for_storage.read(),
        )
        db.session.add(upload_encrypted_file)
        db.session.commit()

        # using pem because it is in byte form
        # upload public RSA key to database
        public_key_file = io.BytesIO()
        public_key_file.write(public_pem)
        public_key_file.seek(0)

        upload_key_file = FileContents(
            user_id=current_user.id,
            name=request.form["file_name"],
            filetype="Public RSA Key File",
            data=public_key_file.read(),
        )
        db.session.add(upload_key_file)
        db.session.commit()

        # using pem because it is in byte form
        private_key_file = io.BytesIO()
        private_key_file.write(private_pem)
        private_key_file.seek(0)

        return send_file(
            private_key_file,
            as_attachment=True,
            attachment_filename=request.form["file_name"] + "_private.key",
            mimetype="text/plain",
        )

    return render_template("rsa/file_encryption.html")


@encryption.route("/rsa/file_decryption", methods=["GET", "POST"])
def rsa_file_decryption():

    # store all of available single key files for display on html template
    user_files = FileContents.query.filter_by(
        user_id=current_user.id, filetype="RSA Encrypted File"
    ).all()

    if request.method == "POST":
        byte_password = bytes(request.form["rsa_key_password"], "utf-8")

        key_file_data = request.files["user_file_rsa_private_key"].read()
        private_key = serialization.load_pem_private_key(
            key_file_data,
            password=byte_password,
        )

        # data saved as base64, must decode for decryption to work
        b64_encrypted_file_data = request.files["user_file_to_decrypt_rsa_file"].read()
        encrypted_file_data = base64.urlsafe_b64decode(b64_encrypted_file_data)

        decrypted_data = private_key.decrypt(
            encrypted_file_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        # using pem because it is in byte form
        decrypted_file = io.BytesIO()
        decrypted_file.write(decrypted_data)
        decrypted_file.seek(0)

        return send_file(
            decrypted_file,
            as_attachment=True,
            attachment_filename="decrypted_rsa",
            mimetype="text/plain",
        )

    return render_template("rsa/file_decryption.html", user_files=user_files)
