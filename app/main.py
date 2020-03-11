# main.py
from pprint import pprint

from flask import Blueprint, request, render_template
from flask_login import login_required, current_user
from sqlalchemy import or_, null

from .models import User
from . import db

main = Blueprint('main', __name__)


@main.route('/index')
@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@main.route('/profile', methods=['POST'])
def profile_post():

    if request.form.get('first_name') is not None and request.form.get('first_name') != "":
        current_user.profile.first_name = request.form.get('first_name')
    if request.form.get('last_name') is not None and request.form.get('last_name') != "":
        current_user.profile.last_name = request.form.get('last_name')
    if request.form.get('country') is not None and request.form.get('country') != "":
        current_user.profile.country = request.form.get('country')
    if request.form.get('city') is not None and request.form.get('city') != "":
        current_user.profile.city = request.form.get('city')
    if request.form.get('antipodal_for_id') is not None and request.form.get('antipodal_for_id') != "":
        current_user.antipodal_for_id = request.form.get('antipodal_for_id')
        antipodal_for = User.query.get(request.form.get('antipodal_for_id'))
        antipodal_for.antipodal_for_id = current_user.id

    db.session.commit()

    return render_template('profile.html')


@main.route('/location')
def location():
    return render_template('location.html')


@main.route('/find_my_location', methods=['POST'])
def find_my_location():
    if request.form.get('city') is not None and request.form.get('city') != "":
        current_user.profile.city = request.form.get('city')
    if request.form.get('country') is not None and request.form.get('country') != "":
        current_user.profile.country = request.form.get('country')

    db.session.commit()

    return render_template('profile.html')


@main.route('/find_friend', methods=['POST'])
def find_friend():
    if request.form.get('country') is not None and request.form.get('country') != "":
        current_user.profile.country = request.form.get('country')
        if request.form.get('city') is not None and request.form.get('city') != "":
            country = request.form.get('country')
            city = request.form.get('city')
            antipodal_of = User.query.\
                filter_by(or_(
                    country=country,
                    city=city,
                    antipodal_for=null))\
                .first()
            antipodal_of.antipodal_for_id = current_user.id
            current_user.antipodal_of_id = antipodal_of.id

    db.session.commit()

    return render_template('profile.html')

