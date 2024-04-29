#!/usr/bin/env python3

"""
Type aliases
"""

from dataclasses import dataclass
import datetime
from typing import Optional

UserToken = str
ChannelId = int
Filename = str
Id = int
Date = datetime.datetime


@dataclass
class QueryArguements:
    """
    Arguements to query the database
    :param keyword: If not None, returns messages only containing the keyword
    :param before_date: If not None, returns messages after the date
    :param after_date: If not None, returns messages before the date
    :param channel: If not None, returns messages from that channel Id
    """

    keyword: Optional[str] = None
    before_date: Optional[Date] = None
    after_date: Optional[Date] = None
    channel: Optional[ChannelId] = None
