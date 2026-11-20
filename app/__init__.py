from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.routes import auth, songs, playlists, recommendations, home
    app.register_blueprint(home.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(songs.bp)
    app.register_blueprint(playlists.bp)
    app.register_blueprint(recommendations.bp)

    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Load recommendation models if they exist
        try:
            from app.recommendation_engine import recommendation_engine
            recommendation_engine.load_models()
        except Exception as e:
            print(f"Warning: Could not load recommendation models: {e}")

    return app 