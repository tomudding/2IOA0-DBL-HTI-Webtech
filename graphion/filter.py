"""
Author(s): Steven van den Broek
Created: 2019-05-18
Edited: 2019-05-31
"""

from flask import Blueprint, redirect, render_template
from graphion import server
from bokeh.embed import server_document
import os
from graphion.graphing.parser import processCSVMatrix
from graphion.upload import set_df, set_filtered_df

filterBlueprint = Blueprint('filterBlueprint', __name__, template_folder='templates')

@filterBlueprint.route('/filter', methods=['GET'], strict_slashes=False)
@filterBlueprint.route('/filter/<file>', methods=['GET'], strict_slashes=False)
def visualise(file=None):
    if file is None:
        return redirect('/selection')
    df = processCSVMatrix(os.path.join(server.config['TEMP_FOLDER'], (file + '.csv')))
    set_df(df)
    set_filtered_df(df)
    # return render_template('filter.html', fileName=file)
    return render_template('filter.html')