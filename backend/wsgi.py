from app import app
from app.routes.api_routes import api_routes

if __name__ == "__main__":
    app.register_blueprint(api_routes)
    app.run()