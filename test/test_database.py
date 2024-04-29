#!/usr/bin/env python3

"""
Test database operations work
"""

import sqlalchemy

from database import Message
from db_models import Database


def create_database() -> Database:
    return Database(sqlalchemy.create_engine("sqlite://", echo=True))


def test_create():
    db = create_database()
    db.create_all_tables()


def test_insert():
    db = create_database()
    messages = [
        Message(
            author_name="test",
            content="this is a message",
            message_id=1,
            channel_id=2,
            channel_name="world",
            message_timestamp=datetime.datetime.now(),
        ),
        Message(
            author_name="test",
            content="this is a message",
            message_id=2,
            channel_id=3,
            channel_name="world",
            message_timestamp=datetime.datetime.now(),
        ),
        Message(
            author_name="test",
            content="this is a message",
            message_id=3,
            channel_id=4,
            channel_name="world",
            message_timestamp=datetime.datetime.now(),
        ),
    ]
    db.insert_messages(messages)


def test_fetch_all():
    db = create_database()
    messages = [
        Message(
            author_name="test",
            content="this is a message",
            message_id=1,
            channel_id=2,
            channel_name="world",
            message_timestamp=datetime.datetime.now(),
        ),
        Message(
            author_name="test",
            content="this is a message",
            message_id=2,
            channel_id=3,
            channel_name="world",
            message_timestamp=datetime.datetime.now(),
        ),
        Message(
            author_name="test",
            content="this is a message",
            message_id=3,
            channel_id=4,
            channel_name="world",
            message_timestamp=datetime.datetime.now(),
        ),
    ]
    db.insert_messages(messages)

    fetched = db.get_messages()
    assert len(fetched) == 3
    assert any(m.message_id == 1 for m in fetched)
    assert any(m.message_id == 2 for m in fetched)
    assert any(m.message_id == 3 for m in fetched)
