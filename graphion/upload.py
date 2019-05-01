"""
Author(s): Tom Udding
Created: 2019-05-01
Edited: 2019-05-01
"""
import os, secrets
from flask import flash, request, redirect, url_for
from graphion import server
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in server.config['ALLOWED_EXTENSIONS']

@server.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            # throw exception because file is not in submitted form
            return redirect('/visualise')
        file = request.files['file']
        if file.filename == '':
            # throw exception because file is still not submitted
            return redirect('/visualise')
        if file and allowed_file(file.filename):
            fileUniqueHash = secrets.token_hex(server.config['TOKEN_SIZE'])
            fileName = fileUniqueHash + '.' + file.filename.split('.')[-1]
            file.save(os.path.join(server.config['UPLOAD_FOLDER'], fileName))
            return redirect('/visualise/' + fileUniqueHash)
    return redirect('/visualise')