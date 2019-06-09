"""
Author(s): Sam Baggen, Tom Uddnig
Created: 2019-06-06
Edited: 2019-06-09
"""
from flask import Blueprint, request
from graphion import server
from graphion.graphing.generator import changePalette

apiPaletteBlueprint = Blueprint('apiPaletteBlueprint', __name__, template_folder='templates')

@apiPaletteBlueprint.route('/switch-palette', methods = ['POST'])
def worker():
    sid = request.cookies.get(server.config['SESSION_COOKIE_NAME'])
    new_palette = request.form['to']
    changePalette(new_palette, sid)
    return "new color palette succesfully applied"