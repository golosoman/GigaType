from flask import Blueprint
from app.api.user import user_api
from app.api.difficulty import difficulty_api
from app.api.task import task_api
from app.api.statistic import statistic_api

api_routes = Blueprint("api_routes", __name__, url_prefix="/api")

api_routes.register_blueprint(user_api)
api_routes.register_blueprint(difficulty_api)
api_routes.register_blueprint(task_api)
api_routes.register_blueprint(statistic_api)
