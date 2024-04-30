#!/usr/bin/env python3

"""
Common + Core Types that work with the database
"""

import datetime
from typing import Any, Callable, List, Tuple
from typing import Optional
import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Query, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Engine, Select, select

from .models import Message
from .type_aliases import QueryArguements

# ===== DB Tables ============


class Base(DeclarativeBase):
    pass


class DBMessage(Base):
    """Table storing all the discord messages"""

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)

    author_name: Mapped[str]
    content: Mapped[str]
    message_id: Mapped[int]
    channel_id: Mapped[int]
    channel_name: Mapped[str]
    message_timestamp: Mapped[datetime.datetime]


# ===== DB Object Conversions ============


def message_to_db_message(message: Message) -> DBMessage:
    """
    Converts the model Message to the Database Message object
    """
    return DBMessage(
        author_name=message.author_name,
        content=message.content,
        message_id=message.message_id,
        channel_id=message.channel_id,
        channel_name=message.channel_name,
        message_timestamp=message.message_timestamp,
    )


def db_message_to_message(db_message: DBMessage) -> Message:
    """
    Converts the Database Message object to a model Message
    """
    return Message(
        author_name=db_message.author_name,
        content=db_message.content,
        message_id=db_message.message_id,
        channel_id=db_message.channel_id,
        channel_name=db_message.channel_name,
        message_timestamp=db_message.message_timestamp,
    )


# ===== Database ============


class Database:
    """
    Interface to interact with the database, and run SQL Alchemy code with
    """

    engine: Engine

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def create_all_tables(self) -> None:
        """Creates all database tables"""
        Base.metadata.create_all(self.engine)

    def insert_messages(self, messages: List[Message]):
        """
        Inserts `messages` into the table
        """
        with Session(self.engine) as session:
            db_messages: List[DBMessage] = list(
                map(lambda msg: message_to_db_message(msg), messages)
            )

            session.add_all(db_messages)
            session.commit()

    def get_messages(self, query: QueryArguements = QueryArguements()) -> List[Message]:
        """
        Gets messages from the database, filtered based on `query`
        """
        insp = sqlalchemy.inspect(self.engine)
        if not insp.has_table(DBMessage.__tablename__):
            return []

        # Helper Type classes
        WhereClause = Callable[[Select[Tuple[Any]]], Select[Any]]

        # Helper clause that does nothing, for unconstraining where clauses
        NO_OP_CLAUSE: WhereClause = lambda q: q

        date_clause: WhereClause = NO_OP_CLAUSE
        keyword_clause: WhereClause = NO_OP_CLAUSE
        channel_clause: WhereClause = NO_OP_CLAUSE

        # Dates
        if query.before_date and query.after_date:
            date_clause = lambda q: q.where(
                DBMessage.message_timestamp >= query.before_date
            ).where(DBMessage.message_timestamp <= query.after_date)
        if query.before_date:
            date_clause = lambda q: q.where(
                DBMessage.message_timestamp <= query.before_date
            )
        if query.after_date:
            date_clause = lambda q: q.where(
                DBMessage.message_timestamp >= query.after_date
            )

        # Keyword
        if query.keyword:
            keyword_clause = lambda q: q.where(
                DBMessage.content.contains(query.keyword)
            )

        # Channel
        if query.channel:
            channel_clause = lambda q: q.where(DBMessage.channel_id == query.channel)

        messages: List[Message] = []

        with Session(self.engine) as session:
            stmt = select(DBMessage)
            stmt = date_clause(stmt)
            stmt = keyword_clause(stmt)
            stmt = channel_clause(stmt)

            for message in session.scalars(stmt):
                messages.append(db_message_to_message(message))
                print(message)

        return messages
