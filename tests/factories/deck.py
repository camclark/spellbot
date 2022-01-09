import factory

from spellbot.models import Deck


class DeckFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: 50 + n)
    name = factory.Faker("name")
    link = factory.Faker("url")

    class Meta:
        model = Deck
        sqlalchemy_session_persistence = "flush"
