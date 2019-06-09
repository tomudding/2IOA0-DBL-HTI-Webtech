"""
Author(s): Tom Udding
Created: 2019-05-01
Edited: 2019-06-09
"""
from flask import Blueprint, render_template, session
from glob import glob
from graphion import server
from os import listdir
from os.path import basename, getctime, join
from pandas import HDFStore

selectionBlueprint = Blueprint('selectionBlueprint', __name__, template_folder='templates')

@selectionBlueprint.route('/selection', methods=['GET'])
def selection():
    if session.get("active", None) is None:
        session['active'] = True
    recentlyUploadedFiles = getRecentlyUploaded()
    return render_template('selection.html', filesList=recentlyUploadedFiles)

def getRecentlyUploaded():
    listOfFiles = sorted([join(server.config['UPLOAD_FOLDER'], f) for f in listdir(server.config['UPLOAD_FOLDER']) if f.endswith('.h5')], key=getctime, reverse=True)[:20]
    finalListOfFiles = {}
    for file in listOfFiles:
        with HDFStore(file) as currentFile:
            id = basename(currentFile.filename)[0:-3]
            finalListOfFiles[id] = next(iter(currentFile.keys()), None).lstrip("/")
    return finalListOfFiles