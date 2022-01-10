import logging

from discord_slash.context import InteractionContext

from .. import SpellBot
from .base_interaction import BaseInteraction
from ..operations import safe_send_channel

logger = logging.getLogger(__name__)


class MetaInteraction(BaseInteraction):
    def __init__(self, bot: SpellBot, ctx: InteractionContext):
        super().__init__(bot, ctx)

    async def deck_add(self, user_xid: int, name: str, link: str):
        assert self.ctx
        await self.services.metas.deck_add(user_xid=user_xid, name=name, link=link)
        await safe_send_channel(self.ctx, "added")
