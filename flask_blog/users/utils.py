
import os
# Модуль secrets содержит функции для создания безопасных токенов,
# используемых при процедурах сброса пароля, обновления важных параметров и т.д.
# Строка содержит 8 случайных байтов, каждый из которых трансформируется в две 16x цифры
from secrets import token_hex
# PIL - библиотека для работы с изображениями
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
# компонент пользовательский, но не встроенный - следует зарегитрировать его в __init__.py
from flask_blog import mail


def save_picture(form_picture):
    """функция обеспечивает изменение аватарки пользователя"""
    # Функция token_hex() возвращает случайную строку в шестнадцатеричном формате
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    # Запрашиваем токен, который по сути является электронной подписью, которая гарантирует безопасность доставки
    token = user.get_reset_token()
    # Создаем объект сообщения, в котором определяем email-ы отправителя и получателя
    msg = Message('Password Reset Request', sender='dlinnii21@gmail.com', recipients=[user.email])
    # Определяем тело сообщения и указываем в нем ссылку, которая обеспечит запуск процедуры переустановки пароля.
    msg.body = f'''To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)
