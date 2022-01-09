from tests.fixtures import Factories


class TestModelDeck:
    def test_deck(self, factories: Factories):
        user = factories.user.create()
        deck = factories.deck.create(user=user)

        assert deck.to_dict() == {
            "id": deck.id,
            "created_at": deck.created_at,
            "updated_at": deck.updated_at,
            "name": deck.name,
            "link": deck.link,
            "user_xid": deck.user_xid,
        }
        assert user.xid == deck.user_xid
