import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool

from sources.database import Base
from .factories import UserFactory

SQLALCHEMY_TEST_DATABASE_URL = "sqlite://"


@pytest.fixture(scope="session")
def connection(request):
    engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL,
                           connect_args={'check_same_thread': False},
                           poolclass=StaticPool, echo=True)
    connection = engine.connect()

    def teardown():
        connection.close()

    request.addfinalizer(teardown)
    return connection


@pytest.fixture(scope="session", autouse=True)
def setup_db(connection, request):
    Base.metadata.bind = connection
    Base.metadata.create_all()

    def teardown():
        Base.metadata.drop_all()

    request.addfinalizer(teardown)


@pytest.fixture(autouse=True)
def session(connection, setup_db, request):
    engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
    Session = scoped_session(sessionmaker(engine))

    transaction = connection.begin()
    session = Session(bind=connection)
    session.begin_nested()
    UserFactory._meta.sqlalchemy_session = session

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(db_session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.expire_all()
            session.begin_nested()

    def teardown():
        Session.remove()
        transaction.rollback()

    request.addfinalizer(teardown)
    return session
