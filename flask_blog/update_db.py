# функция, отвечающая за создание объекта Flask-приложения
from flask_blog import create_app
# объект подсистемы для работы с базой данных средствами библиотеки SQLAlchemy
from flask_blog import db

app = create_app()
app.app_context().push()
db.drop_all()
db.create_all()
