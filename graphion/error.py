"""
Author(s): Tom Udding
Created: 2019-04-29
Edited: 2019-04-29
"""
from graphion import server
from flask import render_template

@server.errorhandler(403)
def not_allowed(error):
    return render_template('errors/403.html'), 403

@server.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@server.errorhandler(405)
def method_not_allowed(error):
    return render_template('errors/405.html'), 405

@server.errorhandler(413)
def size_exceeded(error):
    return render_template('errors/413.html'), 413

@server.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500