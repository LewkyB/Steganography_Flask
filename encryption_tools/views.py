from flask import Blueprint, render_template, send_file
from flask_login import current_user
from encryption_tools.models import FileContents
import io


views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def index():

    return render_template("home.html")


@views.route("/profile")
def profile():

    user_files = []

    user_files = FileContents.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "profile.html", name=current_user.name, user_files=user_files
    )


@views.route("/download/<int:id>", methods=["GET"])
def download_blob(id):

    file_query = FileContents.query.filter_by(id=id).first()
    file_to_download = file_query.data
    download_name = file_query.name
    return send_file(
        io.BytesIO(file_to_download),
        attachment_filename=download_name,
        mimetype="text/plain",
    )
