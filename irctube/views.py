from flask import Blueprint, render_template
from flask_login import current_user
from irctube.models import FileContents
from . import db


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
