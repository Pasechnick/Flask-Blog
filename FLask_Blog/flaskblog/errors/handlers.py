from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

# we treat this almost as a route
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404 # second value 404 is a status code (in flask we can return a second value that is a status code)

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/404.html'), 500