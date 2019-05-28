"""
Author(s): Steven van den Broek
Created: 2019-05-18
Edited: 2019-05-18
"""

from flask import Blueprint, redirect, render_template
from graphion import server
from bokeh.embed import server_document
import os
from graphion.graphing.parser import processCSVMatrix

filterBlueprint = Blueprint('filterBlueprint', __name__, template_folder='templates')

@filterBlueprint.route('/filter', methods=['GET'], strict_slashes=False)
@filterBlueprint.route('/filter/<file>', methods=['GET'], strict_slashes=False)
def visualise(file=None):
    if file is None:
        return redirect('/selection')
    global df
    df = processCSVMatrix(os.path.join(server.config['TEMP_FOLDER'], (file + '.csv')))
    return render_template('filter.html', fileName=file)

def get_df():
    return df