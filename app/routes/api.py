import datetime
from functools import wraps

import jwt
from flask import request, jsonify, make_response, Blueprint, current_app
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import User
from app.extensions import db

api = Blueprint('api', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@api.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.is_admin:
        return jsonify({'message': 'Cannot perform that function!'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {'id': user.id,
                     'username': user.username,
                     'email': user.email}
        output.append(user_data)

    return jsonify({'users': output})


@api.route('/user/<id>', methods=['GET'])
@token_required
def get_one_user(current_user, id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user_data = {'id': user.id,
                 'username': user.username,
                 'email': user.email}

    return jsonify({'user': user_data})


@api.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()

    # check if user already exists in database
    user = User.query.filter_by(email=data['email']).first()
    # redirect to signup page to try again if user with same email is found
    if user:
        return jsonify({'message': 'User with same email already exists.'})
    # create new user using inputted data; password is encrypted from plaintext
    new_user = User(email=data['email'],
                    username=data['username'],
                    password=generate_password_hash(data['password'], method='sha256'))
    # add new user to database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


# @api.route('/user/<id>', methods=['PUT'])
# # @token_required
# def promote_user(current_user, id):
#     if not current_user.admin:
#         return jsonify({'message': 'Cannot perform that function!'})
#
#     user = User.query.filter_by(id=id).first()
#
#     if not user:
#         return jsonify({'message': 'No user found!'})
#
#     user.admin = True
#     db.session.commit()
#
#     return jsonify({'message': 'The user has been promoted!'})


@api.route('/user/<id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted!'})


@api.route('/login-api')
def login():
    auth = request.authorization
    remember = True if request.form.get('remember') else False

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': user.id,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           current_app.config['SECRET_KEY'])
        login_user(user, remember=remember)
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
