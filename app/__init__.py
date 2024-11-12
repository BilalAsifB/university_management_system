from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

# Database initialization
db = SQLAlchemy()

def create_app():
    # Flask application creation
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialization SQLAlchemy with app
    db.init_app(app)

    # Register routes and other app components
    with app.app_context():
        from . import routes
        db.create_all() # table creation (if doesn't exist)
        routes.init_app(app)

    return app
