from app.models import User


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email is defined correctly
    """
    assert new_user.email == 'mo@mo.mo'
