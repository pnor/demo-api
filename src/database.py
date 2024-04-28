#!/usr/bin/env python3

from typing import List, Dict, Any
from models import Message
from type_aliases import ChannelId, Date, Filename, UserToken

import sqlalchemy.orm  # ...

# ===== "Public" functions ===============


class MessageTable(db.model):
    pass


# https://docs.sqlalchemy.org/en/20/orm/quickstart.html
def store_messages_in_database(messages: List[Message]) -> bool:
    """
    Stores `messages` into the database
    """
    pass
