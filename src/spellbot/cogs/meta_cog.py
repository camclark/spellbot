import logging

from ddtrace import tracer
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.model import SlashCommandOptionType

from .. import SpellBot
from ..interactions import MetaInteraction
from ..metrics import add_span_context
from ..utils import for_all_callbacks

logger = logging.getLogger(__name__)


@for_all_callbacks(commands.guild_only())
class MetaCog(commands.Cog):
    def __init__(self, bot: SpellBot):
        self.bot = bot

    @cog_ext.cog_subcommand(
        base="deck",
        name="add",
        description="Create a new deck with a name and link.",
        options=[
            {
                "name": "name",
                "description": "A name for this deck.",
                "required": True,
                "type": SlashCommandOptionType.STRING.value,
            },
            {
                "name": "link",
                "description": "A link to your decklist.",
                "required": True,
                "type": SlashCommandOptionType.STRING.value,
            },
        ],
    )
    @tracer.wrap(name="interaction", resource="meta")
    async def deck_add(self, ctx: SlashContext, name: str, link: str):
        add_span_context(ctx)
        async with MetaInteraction.create(self.bot, ctx) as interaction:
            await interaction.deck_add(user_xid=ctx.author_id, name=name, link=link)


def setup(bot: SpellBot):
    bot.add_cog(MetaCog(bot))
