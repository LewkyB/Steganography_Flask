from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename

from . import db

import os

from irctube import app

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('home.html')

@views.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/upload_success', methods = ['GET', 'POST'])
def get_file():

    if request.method == 'POST':
        file_from_user = request.files['user_image_file']
        filename = secure_filename(file_from_user.filename)
        file_from_user.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        text = request.form['message_to_encrypt_textbox']
        processed_text = text.upper()

        return render_template('upload_success.html', filename=filename)
