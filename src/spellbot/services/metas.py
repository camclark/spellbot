# pylint: disable=wrong-import-order

from asgiref.sync import sync_to_async

from ..database import DatabaseSession
from ..models import Deck


class MetasService:
    @sync_to_async()
    def deck_add(self, user_xid: int, name: str, link: str) -> None:
        DatabaseSession.add(Deck(user_xid=user_xid, name=name, link=link))
        DatabaseSession.commit()
