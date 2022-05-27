from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def init_app():
    """Initialize the core application."""
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():
        # Include our Routes
        from app import routes

        # Register Blueprints
        app.register_blueprint(routes.main_bp)
 

        # Create Database Models
        db.create_all()

        return app