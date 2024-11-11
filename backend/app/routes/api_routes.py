from flask import Blueprint
from backend.app.api.user import user_api

api_routes = Blueprint("api_routes", __name__, url_prefix="/api")

api_routes.register_blueprint(user_api)
