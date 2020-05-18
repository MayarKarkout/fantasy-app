# main.py
from pprint import pprint

from flask import Blueprint, request, render_template
from flask_login import login_required, current_user
from sqlalchemy import or_, null

from app.models import User, FantasyTeam
from app import db

main = Blueprint('main', __name__)


@main.route('/index')
@main.route('/')
def index():
    return render_template('index.html')


@main.route('/fantasy_team')
@login_required
def fantasy_team():
    return render_template('fantasy_team.html')


@main.route('/fantasy_team', methods=['POST'])
def fantasy_team_post():

    if request.form.get('name') is not None and request.form.get('name') != "":
        current_user.fantasy_team = FantasyTeam(name=request.form.get('name'))

    db.session.commit()

    return render_template('fantasy_team.html')


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

