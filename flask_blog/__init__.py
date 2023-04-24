from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_blog.config import Config
from flask_bcrypt import Bcrypt


db = SQLAlchemy()

# подключение системы аутентификации
login_manager = LoginManager()

bcrypt = Bcrypt()

mail = Mail()


def create_app():
    print(__name__)
    app = Flask(__name__)
    # подключаем конфиг, обязательно в начале скрипта
    app.config.from_object(Config)
    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate = Migrate(app, db)

    from flask_blog.users.routes import users
    from flask_blog.main.routes import main
    from flask_blog.posts.routes import posts
    from flask_blog.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)


    return app
