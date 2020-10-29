from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskblog.config import Config
from flask_misaka import Misaka


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.categories.routes import categories
    from flaskblog.errors.handlers import errors

    app.config.from_object(Config)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(categories)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    bcrypt.init_app(app)
    login_manager.init_app(app)
    md = Misaka(footnotes=True, tables=True)
    md.init_app(app)

    return app
