from flask import render_template, request
from werkzeug.utils import secure_filename
import json
import os

from irctube import app

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/upload_success', methods = ['GET', 'POST'])
def get_file():

    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        
        text = request.form['text']
        processed_text = text.upper()

        return render_template('upload_success.html')
