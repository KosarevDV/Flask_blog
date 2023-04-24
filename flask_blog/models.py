from datetime import datetime, timezone, timedelta

from jwt import decode, encode

from flask_blog import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    # backref='author' - указание на запись в модели Post, чтобы можно было отслеживать кто автор записи блога.
    # lazy=True - связанные записи наших двух таблиц («пользователи» и «посты») будут загружаться параллельно.
    posts = db.relationship('Post', backref='author', lazy=True)

    # def get_reset_token(self, expires_sec=1800):
    #     s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
    #     return s.dumps({'user_id': self.id}).decode('utf-8')
    #
    # @staticmethod
    # def verify_reset_token(token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         user_id = s.loads(token)['user_id']
    #     except Exception:
    #         return None
    #     return User.query.get(user_id)

    def get_reset_token(self, expires_sec=1800):
        # Определяем параметры пользователя, на основе которых будем создавать токен: ид пользователя, срок действия
        payload = {'user_id': self.id, 'exp': datetime.now(timezone.utc) + timedelta(seconds=expires_sec)}
        # Выполняем сериализацию параметров, используя секретный ключ и алгоритм шифрования
        return encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

    @staticmethod
    def verify_reset_token(token, leeway=10):
        """десериализация ключа"""
        try:
            # расшифровка токена. leeway - отсрочка действия токена еще на 10 секунд
            data = decode(token, current_app.config['SECRET_KEY'], leeway=leeway, algorithms=['HS256'])
        except Exception:
            return None
        return User.query.get(data['user_id'])

    def __repr__(self):
        return f"Пользователь('{self.username}','{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    # каскадного удаления комментариев при удалении поста
    comments = db.relationship('Comment', backref='title', lazy='select', cascade='all, delete-orphan')

    def __repr__(self):
        return f"Запись('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    username = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)


class Like(db.Model):
    __table_args__ = (db.PrimaryKeyConstraint('user_id', 'post_id', name='CompositePkForLike'),)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.String(36), db.ForeignKey('post.id'), nullable=False)
