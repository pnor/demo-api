#!/usr/bin/env python3

import datetime
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

from . import type_aliases

"""
Core types sent in the API
"""


# - Server API Requests -


class Download(BaseModel):
    user_token: type_aliases.UserToken
    channel: type_aliases.ChannelId


class GetReq(BaseModel):
    user_token: type_aliases.UserToken
    keyword: Optional[str] = None
    before_date: Optional[datetime.datetime] = None
    after_date: Optional[datetime.datetime] = None
    channel_id: Optional[type_aliases.ChannelId] = None


# - Objects Sent and Created -


class Message(BaseModel):
    author_name: str
    content: str
    message_id: type_aliases.Id
    channel_id: type_aliases.ChannelId
    channel_name: str
    message_timestamp: type_aliases.Date
