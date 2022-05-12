from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)

    if not test_config:
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
        
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.book import Book 
    from app.models.author import Author 
    from app.models.genre import Genre
    from app.models.book_genre import BookGenre

    # Book Model 
    from .book_routes import books_bp
    app.register_blueprint(books_bp)
    # Author Model 
    from .author_routes import authors_bp
    app.register_blueprint(authors_bp)
    # Genre Model 
    from .genre_routes import genres_bp
    app.register_blueprint(genres_bp)
    

    # Can ignore hello_world code below, that is for another blueprint
    # from .routes import hello_world_bp
    # app.register_blueprint(hello_world_bp)

    return app