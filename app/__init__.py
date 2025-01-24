from flask import Flask
from app.routes import bp as routes_bp

def create_app():
    """
    Application factory that creates and configures the Flask app instance.
    """
    app = Flask(__name__)

    # Register the routes blueprint
    app.register_blueprint(routes_bp)

    return app
