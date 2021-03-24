from flask import Flask 

app = Flask(__name__)

from irctube import views, commands  # noqa: F401
