from flask import Blueprint

api_v1 = Blueprint('admin-api', __name__)

from app.routes.api.admin import routes