import pytest
from app.models import *
from app import create_app, db
# from config import TestConfig
from werkzeug.security import generate_password_hash


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    # db.create_all()

    # Insert user data
    user1 = User(email='test@user.com', username='Flask', password=generate_password_hash('hi', method='sha256'))
    user2 = User(email='test@user1.com', username='PaSsWoRd', password='hi2')
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    # db.session.commit()

    try:
        # db.session.begin_nested()
        yield db.session
    finally:
        db.session.rollback()
        db.session.close()


@pytest.fixture(scope='module')
def new_user():
    new_user = User(id=11,
                    username='mo',
                    email='mo@mo.mo',
                    password='hi')
    return new_user


@pytest.fixture(scope='module')
def new_profile():
    new_profile = Profile(id=12,
                          first_name='fname',
                          last_name='lname')
    return new_profile


@pytest.fixture(scope='module')
def new_fantasy_team():
    new_fantasy_team = FantasyTeam(id=13,
                                   name='bestteam',
                                   overall_score=100)
    return new_fantasy_team


@pytest.fixture(scope='module')
def new_player():
    new_player = Player(id=14,
                        number=10,
                        first_name='smallboy',
                        last_name='bigboy',
                        nickname='sha256')
    return new_player


@pytest.fixture(scope='module')
def new_team():
    new_team = Team(id=15,
                    name='sww')
    return new_team


@pytest.fixture(scope='module')
def new_fantasy_teams():
    new_fantasy_team1 = FantasyTeam(id=16,
                                    name='fteam1',
                                    overall_score='101')
    new_fantasy_team2 = FantasyTeam(id=17,
                                    name='fteam2',
                                    overall_score='102')
    new_fantasy_team3 = FantasyTeam(id=18,
                                    name='fteam3',
                                    overall_score='103')
    new_fantasy_teams = [new_fantasy_team1, new_fantasy_team2, new_fantasy_team3]

    return new_fantasy_team


@pytest.fixture(scope='module')
def new_players():
    new_player1 = Player(id=19,
                         number=11,
                         first_name='fname1',
                         last_name='lname1',
                         nickname='nname1')
    new_player2 = Player(id=20,
                         number=12,
                         first_name='fname2',
                         last_name='lname2',
                         nickname='nname2')
    new_player3 = Player(id=21,
                         number=13,
                         first_name='fname3',
                         last_name='lname3',
                         nickname='nname3')

    new_players = [new_player1, new_player2, new_player3]

    return new_players


def delete_fantasy_team(fantasy_team):
    db.session.delete(fantasy_team)
