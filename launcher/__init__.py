import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    # 블루프린트
    from .views import auth_views, main_views, book_views, board_views
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(main_views.bp)
    app.register_blueprint(book_views.bp)
    app.register_blueprint(board_views.bp)

    return app

if __name__ == '__main__':
    db.create_all()
    app.run('localhost', port=5000, debug=True)