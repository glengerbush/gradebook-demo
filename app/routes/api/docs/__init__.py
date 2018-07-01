from flask import Blueprint

api = Blueprint('docs-api', __name__)

from app.routes.api.docs import routes
