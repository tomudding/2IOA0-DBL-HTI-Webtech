"""
Author(s): Tom Udding, Steven van den Broek
Created: 2019-05-01
Edited: 2019-06-02
"""
import os, secrets
from flask import flash, request, redirect
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
            set_df(df)
            df.to_hdf(os.path.join(server.config['UPLOAD_FOLDER'], (fileUniqueHash + '.h5')), key=fileUniqueHash)
            return redirect('/visualise/' + fileUniqueHash)
    return redirect('/selection')

def get_df():
    global df
    if 'df' not in globals():
        return None
    return df.copy()

def set_df(input):
    global df
    global directed
    global sparce
    df = input
    if df.equals(df.transpose()):
        directed = False
    else:
        directed = True
    print("This dataset is directed: " + str(directed))
    if (df.astype(bool).sum(axis=0).sum())/(df.size) > 0.5:
        sparce = False
    else:
        sparce = True
    print("This dataset is sparce: " + str(sparce))

def get_filtered_df():
    if 'filtered_df' in globals():
        if filtered_df is not None:
            return filtered_df.copy()
    if 'almost_filtered_df' in globals():
        if almost_filtered_df is not None:
            return almost_filtered_df.copy()
    if 'partially_filtered_df' in globals():
        if almost_filtered_df is not None:
            return partially_filtered_df.copy()
    return get_df()

def set_filtered_df(input):
    global filtered_df
    filtered_df = input

def get_partially_filtered_df():
    global partially_filtered_df
    if 'partially_filtered_df' in globals():
        if partially_filtered_df is not None:
            return partially_filtered_df.copy()
    return get_df()

def set_partially_filtered_df(input):
    global partially_filtered_df
    partially_filtered_df = input

def get_almost_filtered_df():
    global almost_filtered_df
    if 'almost_filtered_df' in globals():
        if almost_filtered_df is not None:
            return almost_filtered_df.copy()
    return get_df()

def set_almost_filtered_df(input):
    global almost_filtered_df
    almost_filtered_df = input

def is_sparce():
    return sparce

def is_directed():
    return directed