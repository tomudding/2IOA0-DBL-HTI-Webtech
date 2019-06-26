"""
Author(s): Tom Udding, Steven van den Broek
Created: 2019-05-01
Edited: 2019-06-21
"""
from flask import Blueprint, flash, request, redirect, session, abort
from graphion import server
from graphion.graphing.parser import processCSVMatrix, processEdgeList
from os import remove
from os.path import join
from secrets import token_hex
from tempfile import NamedTemporaryFile
from werkzeug import exceptions
from werkzeug.formparser import parse_form_data
from werkzeug.utils import secure_filename

uploadBlueprint = Blueprint('uploadBlueprint', __name__)

def allowed_matrix(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in server.config['ALLOWED_EXTENSIONS_MATRIX']

def allowed_edgelist(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in server.config['ALLOWED_EXTENSIONS_EDGELIST']

@uploadBlueprint.route('/upload_matrix', methods=['GET', 'POST'])
def upload_matrix():
    if request.method == 'POST':
        fileUniqueHash = token_hex(server.config['TOKEN_SIZE'])

        def custom_stream_factory(total_content_length, filename, content_type, content_length=None):
            if total_content_length > server.config['MAX_CONTENT_LENGTH_MATRIX']:
                raise exceptions.RequestEntityTooLarge()
            if not allowed_matrix(filename):
                raise exceptions.ImATeapot()
            tmpfile = NamedTemporaryFile('wb+', delete=False) # delete=False requires manual deletion using os.remove(tmpfile.name)
            return tmpfile

        stream, form, files = parse_form_data(request.environ, stream_factory=custom_stream_factory)

        file = next(iter(files.values()))
        fileOriginalName = secure_filename(file.filename)
        df = processCSVMatrix(file.stream.name)
        df.to_hdf(join(server.config['UPLOAD_FOLDER'], (fileUniqueHash + '.h5')), key=fileOriginalName, complib='blosc:snappy', complevel=9)
        file.stream.close()
        remove(file.stream.name)
        return fileUniqueHash
    return redirect('/selection')

@uploadBlueprint.route('/upload_edgelist', methods=['GET', 'POST'])
def upload_edgelist():
    if request.method == 'POST':
        fileUniqueHash = token_hex(server.config['TOKEN_SIZE'])

        def custom_stream_factory(total_content_length, filename, content_type, content_length=None):
            if total_content_length > server.config['MAX_CONTENT_LENGTH_EDGELIST']:
                raise exceptions.RequestEntityTooLarge()
            if not allowed_edgelist(filename):
                raise exceptions.ImATeapot()
            tmpfile = NamedTemporaryFile('wb+', delete=False) # delete=False requires manual deletion using os.remove(tmpfile.name)
            return tmpfile

        stream, form, files = parse_form_data(request.environ, stream_factory=custom_stream_factory)

        file = next(iter(files.values()))
        fileOriginalName = secure_filename(file.filename)
        df = processEdgeList(file.stream.name)
        df.to_hdf(join(server.config['UPLOAD_FOLDER'], (fileUniqueHash + '.h5')), key=fileOriginalName, complib='blosc:snappy', complevel=9)
        file.stream.close()
        remove(file.stream.name)
        return fileUniqueHash
    return redirect('/selection')