"""
Author(s): Tom Udding, Steven van den Broek
Created: 2019-05-01
Edited: 2019-06-09
"""
import os, secrets
from flask import flash, request, redirect, session
from graphion import server
from graphion.graphing.parser import processCSVMatrix
from tempfile import NamedTemporaryFile
from werkzeug.formparser import parse_form_data
from werkzeug.utils import secure_filename

@server.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # all server-side checks have been removed because they stop the stream
        # I am figuring out how we should do them on the server
        fileUniqueHash = secrets.token_hex(server.config['TOKEN_SIZE'])

        def custom_stream_factory(total_content_length, filename, content_type, content_length=None):
            tmpfile = NamedTemporaryFile('wb+', delete=False) # delete=False requires manual deletion using os.remove(tmpfile.name)
            return tmpfile

        stream, form, files = parse_form_data(request.environ, stream_factory=custom_stream_factory)

        file = next(iter(files.values()))
        fileOriginalName = secure_filename(file.filename.rsplit('.', 1)[0].lower())
        df = processCSVMatrix(file.stream.name)
        df.to_hdf(os.path.join(server.config['UPLOAD_FOLDER'], (fileUniqueHash + '.h5')), key=fileOriginalName)
        file.stream.close()
        os.remove(file.stream.name)
        return fileUniqueHash
    return redirect('/selection')