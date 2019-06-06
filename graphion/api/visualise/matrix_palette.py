"""
Author(s): Sam Baggen
Created: 2019-06-06
Edited: 2019-06-06
"""
from flask import Blueprint, request
from graphion.graphing.generator import changePalette

apiPaletteBlueprint = Blueprint('apiPaletteBlueprint', __name__, template_folder='templates')

@apiPaletteBlueprint.route('/switch-palette', methods = ['POST'])
def worker():
    new_palette = request.form['to']
    changePalette(new_palette)
    return "new color palette succesfully applied"