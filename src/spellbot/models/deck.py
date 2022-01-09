from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base, now

if TYPE_CHECKING:  # pragma: no cover
    from . import User  # noqa


class Deck(Base):
    """Represents a user's decklist."""

    __tablename__ = "decks"

    id = Column(
        Integer,
        autoincrement=True,
        nullable=False,
        primary_key=True,
        doc="This deck's reference ID",
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=now,
        doc="UTC timestamp when this deck was first created",
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=now,
        onupdate=datetime.utcnow,
        doc="UTC timestamp when this deck was last updated",
    )
    name = Column(
        String(100),
        nullable=False,
        doc="Given name of this deck",
    )
    link = Column(
        String(255),
        doc="The decklist link for this deck",
    )
    user_xid = Column(
        BigInteger,
        ForeignKey("users.xid", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        index=True,
        doc="The user associated with this deck",
    )

    user = relationship(
        "User",
        back_populates="decks",
        doc="The user that created this deck",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "name": self.name,
            "link": self.link,
            "user_xid": self.user_xid,
        }
