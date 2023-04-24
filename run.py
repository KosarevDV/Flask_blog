from flask_blog.admin import app


if __name__ == '__main__':
    # Режим отладки (debug=True) должен использоваться только на этапе разработки, на локальной машине.
    # В боевых условиях режим отладки нужно отключать
    app.run(debug=True)
