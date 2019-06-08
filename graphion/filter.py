"""
Author(s): Steven van den Broek, Tom Udding
Created: 2019-05-18
Edited: 2019-06-08
"""

from flask import Blueprint, flash, redirect, render_template
from graphion import server
from bokeh.embed import server_document
import os
from graphion.graphing.parser import processCSVMatrix
from graphion.upload import set_df, set_filtered_df, set_almost_filtered_df,set_partially_filtered_df
from pandas import read_hdf

filterBlueprint = Blueprint('filterBlueprint', __name__, template_folder='templates')

@filterBlueprint.route('/filter', methods=['GET'], strict_slashes=False)
@filterBlueprint.route('/filter/<file>', methods=['GET'], strict_slashes=False)
def visualise(file=None):
    if file is None:
        flash("No dataset has been selected. Please select a previously uploaded dataset or upload a new dataset.", "danger")
        return redirect('/selection')

    if not os.path.exists(os.path.join(server.config['UPLOAD_FOLDER'], (file + '.h5'))):
        flash("Dataset could not be found. Please select a previously uploaded dataset or upload a new dataset.", "danger")
        return redirect('/selection')

    df = read_hdf(os.path.join(server.config['UPLOAD_FOLDER'], (file + '.h5'))) # should be done in a memory efficient way (instead of loading the whole file into memory)
    set_df(df)
    return render_template('filter.html', fileName=file)