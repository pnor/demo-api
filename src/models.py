#!/usr/bin/env python3

from fastapi import FastAPI
from pydantic import BaseModel

import type_aliases


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
    id: type_aliases.Id
    channel_id: type_aliases.ChannelId
    channel_name: str
    timestamp: type_aliases.Date
