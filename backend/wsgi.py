from app import app
from app.routes.api_routes import api_routes
from flask_cors import CORS, cross_origin

if __name__ == "__main__":
    cors = CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
    app.register_blueprint(api_routes)
    app.run()