# __init__.py

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from config import Config

# from flask_socketio import SocketIO

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    # blueprint for routes in our app
    from app.users.auth import auth as auth_blueprint
    from app.main.main import main as main_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    db.init_app(app)

    print(config.SQLALCHEMY_DATABASE_URI)
    print(db.app)

    login_manager.init_app(app)
    migrate = Migrate(app, db)

    app.config['SECRET_KEY'] = 'secret!'

    return app


from .models import User


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table,
    # use it in the query for the user
    return User.query.get(int(user_id))

# socketio = SocketIO(app)
# if __name__ == '__main__':
#     socketio.run(app)
# return app
