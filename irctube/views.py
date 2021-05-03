from flask import Blueprint, render_template
from flask_login import current_user

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def index():

    return render_template("home.html")


@views.route("/profile")
def profile():
    return render_template("profile.html", name=current_user.name)
