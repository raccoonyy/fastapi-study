import factory
import factory.fuzzy
from factory.alchemy import SQLAlchemyModelFactory

from sources.models import User


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    name = factory.fuzzy.FuzzyText(length=20)
    access_token = factory.Faker("uuid4")
