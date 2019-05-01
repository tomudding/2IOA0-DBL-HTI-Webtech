"""
Author(s): Tom Udding
Created: 2019-05-01
Edited: 2019-05-01
"""
import hashlib, os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from graphion import server

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in server.config['ALLOWED_EXTENSIONS']

def calculateSHA1Sum(file):
    sha1 = hashlib.sha1()

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
            #return file.
            #tempName = secrets.token_hex(16)
            #fileName = secure_filename(file.filename)
            #if (os.path.isfile(os.path.join(server.config['UPLOAD_FOLDER'], fileName))):
                # throw exception because file with that name already exists
            #    return redirect('/visualise')
            #file.save(os.path.join(server.config['UPLOAD_FOLDER'], fileName))
            return redirect('/visualise')
        return redirect('/visualise')
