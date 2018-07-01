from flask import Blueprint

api_v1 = Blueprint('teachers-api', __name__)

from app.routes.api.teachers import routes
