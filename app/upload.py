"""
Author(s): Tom Udding
Created: 2019-05-01
Edited: 2019-05-01
"""
import os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from app import server

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in server.config['ALLOWED_EXTENSIONS']

@server.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            # throw exception because file is not in submitted form
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            # throw exception because file is still not submitted
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #if (os.path.isfile(filename)):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/')
