from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager
import os


UPLOAD_FOLDER = "./irctube/uploads"
ALLOWED_EXTENSIONS = {"txt"}

app = Flask(__name__)

db = SQLAlchemy(app)
db.init_app(app)
db.create_all()

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # limit file upload to 16mb

app.config["SECRET_KEY"] = "secret-key-goes-here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

from irctube.views import views as main_blueprint

app.register_blueprint(main_blueprint)
from irctube.auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

from irctube.models import User


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))
