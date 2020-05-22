# __init__.py

from flask import Flask
from flask_admin import Admin
from app.AppModelView import AppModelView
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.models import User, Profile, FantasyTeam, Player, Team

from app.extensions import db, login_manager
from config import Config

# from flask_socketio import SocketIO

# init SQLAlchemy so we can use it later in our models
# db = SQLAlchemy()
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config())

    # blueprint for routes in our app
    from app.users.auth import auth as auth_blueprint
    from app.main.main import main as main_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    db.init_app(app)

    admin = Admin(app, template_mode='bootstrap3')
    admin.add_views(AppModelView(User, db.session))
    admin.add_view(AppModelView(Profile, db.session))
    admin.add_view(AppModelView(FantasyTeam, db.session))
    admin.add_view(AppModelView(Team, db.session))
    admin.add_view(AppModelView(Player, db.session))

    # print(config.SQLALCHEMY_DATABASE_URI)
    # print(db.app)

    login_manager.init_app(app)
    migrate = Migrate(app, db, render_as_batch=True)
    print('hi')
    # app.config['SECRET_KEY'] = 'secret!'

    return app


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table,
    # use it in the query for the user
    return User.query.get(int(user_id))

# socketio = SocketIO(app)
# if __name__ == '__main__':
#     socketio.run(app)
# return app
