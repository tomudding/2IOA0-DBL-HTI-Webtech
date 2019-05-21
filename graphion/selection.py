"""
Author(s): Tom Udding
Created: 2019-05-01
Edited: 2019-05-01
"""
from flask import Blueprint, render_template
from glob import glob
from graphion import server
from os import listdir
from os.path import basename, getctime, join

selectionBlueprint = Blueprint('selectionBlueprint', __name__, template_folder='templates')

@selectionBlueprint.route('/selection', methods=['GET'])
def selection():
    recentlyUploadedFiles = getRecentlyUploaded()
    return render_template('selection.html', filesList=recentlyUploadedFiles)

#temporarily for testing
@selectionBlueprint.route('/testfilter', methods=['GET'])
def testfilter():
        return render_template('testfilter.html')

def getRecentlyUploaded():
    listOfFiles = sorted([join(server.config['UPLOAD_FOLDER'], f) for f in listdir(server.config['UPLOAD_FOLDER']) if f.endswith('.info')], key=getctime, reverse=True)[:10]
    finalListOfFiles = {}
    for file in listOfFiles:
        with open(file, 'r') as currentFile:
            id = basename(currentFile.name)[0:-5]
            finalListOfFiles[id] = currentFile.readline()
    return finalListOfFiles