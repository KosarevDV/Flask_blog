# импортируем класс-конструктор для реализации подсистемы «админка»
from flask_admin import Admin
# Импортируем класс-конструктор для представления модели в табличном виде
from flask_admin.contrib.sqla import ModelView
from flask_blog.models import User, Post
# Импортируем объекты подсистемы SQLAlchemy для работы с базой данных
from flask_blog import db
# Импортируем функцию создания объекта приложения
from flask_blog import create_app
# Создаем объект Flask-приложения
app = create_app()
# Создаем объект подсистемы-админки и привязываем к объекту приложения
admin = Admin(app)
# Привязываем объекты представлений к нашей админке
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
