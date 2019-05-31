"""
Author(s): Tom Udding
Created: 2019-05-01
Edited: 2019-05-16
"""
import os, secrets
from flask import flash, request, redirect, url_for
from graphion import server
from graphion.graphing.parser import processCSVMatrix
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in server.config['ALLOWED_EXTENSIONS']

@server.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            # throw exception because file is not in submitted form
            return redirect('/selection')
        file = request.files['file']
        if file.filename == '':
            # throw exception because file is still not submitted
            return redirect('/selection')
        if file and allowed_file(file.filename):
            fileUniqueHash = secrets.token_hex(server.config['TOKEN_SIZE'])
            file.save(os.path.join(server.config['TEMP_FOLDER'], (fileUniqueHash + '.csv')))
            fileOriginalName = secure_filename(file.filename)
            fileOriginalInformation = open(os.path.join(server.config['UPLOAD_FOLDER'], (fileUniqueHash + '.info')), 'w')
            fileOriginalInformation.write(fileOriginalName)
            fileOriginalInformation.close()
            df = processCSVMatrix(os.path.join(server.config['TEMP_FOLDER'], (fileUniqueHash + '.csv')))
            df.to_hdf(os.path.join(server.config['UPLOAD_FOLDER'], (fileUniqueHash + '.h5')), key=fileUniqueHash)
            return redirect('/filter/' + fileUniqueHash)
    return redirect('/selection')


# Dirty test code for javascript filtering, this is basically the old way of doing things
@server.route('/uploadnow', methods=['GET', 'POST'])
def upload_file_now():
    if request.method == 'POST':
        if 'file' not in request.files:
            # throw exception because file is not in submitted form
            return redirect('/selection')
        file = request.files['file']
        if file.filename == '':
            # throw exception because file is still not submitted
            return redirect('/selection')
        if file and allowed_file(file.filename):
            fileUniqueHash = secrets.token_hex(server.config['TOKEN_SIZE'])
            file.save(os.path.join(server.config['TEMP_FOLDER'], (fileUniqueHash + '.csv')))
            fileOriginalName = secure_filename(file.filename)
            fileOriginalInformation = open(os.path.join(server.config['UPLOAD_FOLDER'], (fileUniqueHash + '.info')), 'w')
            fileOriginalInformation.write(fileOriginalName)
            fileOriginalInformation.close()
            df = processCSVMatrix(os.path.join(server.config['TEMP_FOLDER'], (fileUniqueHash + '.csv')))
            df.to_hdf(os.path.join(server.config['UPLOAD_FOLDER'], (fileUniqueHash + '.h5')), key=fileUniqueHash)
            return redirect('/visualise/' + fileUniqueHash)
    return redirect('/selection')