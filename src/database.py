#!/usr/bin/env python3

"""
User Facing API to store and get messages from the database
"""

from typing import List
from models import Message
from type_aliases import QueryArguements

from . import db_models

import sqlalchemy


def _setup_db(database: db_models.Database) -> None:
    database.create_all_tables()


# ===== "Public" functions ===============


# https://docs.sqlalchemy.org/en/20/orm/quickstart.html
def store_messages_in_database(
    databse: db_models.Database, messages: List[Message]
) -> bool:
    """
    Stores `messages` into the database>
    Assumes the dataabse has already been setup, by creating all the tables
    """
    # Assumes the database is setup
    databse.insert_messages(messages)
    return True


def database_query_messages(
    database: db_models.Database, query: QueryArguements
) -> List[Message]:
    """
    Returns all messages from the database, filtered based on `query`
    """
    # TODO
    return []
