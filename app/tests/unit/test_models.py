from app.tests.conftest import delete_fantasy_team


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email is defined correctly
    """
    assert new_user.password == 'hi'
    assert new_user.username == 'mo'
    assert new_user.email == 'mo@mo.mo'


def test_new_profile(new_profile):
    """
    GIVEN a Profile model
    WHEN a new Profile is created
    THEN check the first_name and last_name are defined correctly
    """
    assert new_profile.first_name == 'fname'
    assert new_profile.last_name == 'lname'


def test_new_fantasy_team(new_fantasy_team):
    """
    GIVEN a FantasyTeam model
    WHEN a new FantasyTeam is created
    THEN check the name and overall_score are defined correctly
    """
    assert new_fantasy_team.name == 'bestteam'
    assert new_fantasy_team.overall_score == 100


def test_new_player(new_player):
    """
    GIVEN a Player model
    WHEN a new Player is created
    THEN check the number, first_name, last_name and nickname are defined correctly
    """
    assert new_player.number == 10
    assert new_player.first_name == 'smallboy'
    assert new_player.last_name == 'bigboy'
    assert new_player.nickname == 'sha256'


def test_team(new_team):
    """
    GIVEN a Team model
    WHEN a new Team is created
    THEN check the name is defined correctly
    """
    assert new_team.name == 'sww'

