from flask import Blueprint

teachers = Blueprint('teachers', __name__)

from app.routes.teachers import routes
