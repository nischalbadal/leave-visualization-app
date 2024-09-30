# app/backend/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config

# Initialize the database and JWT manager
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)

    # Register routes inside the app context
    with app.app_context():
        from .routes import api  # Move the import here
        app.register_blueprint(api)

        db.create_all()  # Create all tables

    return app
