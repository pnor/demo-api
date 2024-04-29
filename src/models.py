#!/usr/bin/env python3

from fastapi import FastAPI
from pydantic import BaseModel

import type_aliases

"""
Core types sent in the API
"""


# - Server API Requests -


class StoreChannelReq(BaseModel):
    user_token: type_aliases.UserToken
    channel: type_aliases.ChannelId


class GetAllReq(BaseModel):
    user_token: type_aliases.UserToken
    channel_id: type_aliases.ChannelId


class GetKeywordReq(BaseModel):
    user_id: type_aliases.Id
    channel: type_aliases.ChannelId
    keyword: str


# - Objects Sent and Created -


class Message(BaseModel):
    author_name: str
    content: str
    message_id: type_aliases.Id
    channel_id: type_aliases.ChannelId
    channel_name: str
    message_timestamp: type_aliases.Date
