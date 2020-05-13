import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'app.db')

    print(SQLALCHEMY_DATABASE_URI)
    print("AAA HAHA HAffHHA")
    # print(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = True

    BCRYPT_LOG_ROUNDS = 15
    # app.config['SECRET_KEY'] = 'secret!'


# class TestConfig:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
#
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#         'sqlite:///' + os.path.join(BASEDIR, 'app_test.db')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#
#     print('YAS WE ARE TESTIN')
#
#     TESTING = True
#     DEBUG = True
#
#     BCRYPT_LOG_ROUNDS = 4
#     WTF_CSRF_ENABLED = False

    # app.config['SECRET_KEY'] = 'secret!'
