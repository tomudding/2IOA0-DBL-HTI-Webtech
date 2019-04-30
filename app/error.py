"""
Author(s): Tom Udding
Created: 2019-04-29
Edited: 2019-04-29
"""
from app import server
from flask import render_template

@server.errorhandler(403)
def not_allowed(error):
    return render_template('errors/403.html'), 403

@server.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@server.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500