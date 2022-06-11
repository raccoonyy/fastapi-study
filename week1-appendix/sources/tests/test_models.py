from sources.models import User, get_users
from .factories import UserFactory


def test_get_users(session):
    UserFactory.create()
    assert session.query(User).one()

    assert len(get_users(session)) == 1
