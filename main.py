#!/usr/bin/env python3

from typing import Union

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from src.db_models import Database
from src.discord_download import get_messages_from_last_7_days
from src.models import Download, GetReq

from src.type_aliases import QueryArguements

import sys

print(sys.path)

app = FastAPI()

database = Database(create_engine("sqlite://", echo=True))
database.create_all_tables()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/download", status_code=201)
def download_from_discord(download: Download):
    database.create_all_tables()
    try:
        messages = get_messages_from_last_7_days(download.user_token, download.channel)
    except:
        raise HTTPException(status_code=400, detail="Unable to export discord")
    database.insert_messages(messages)
    return {"success": True}


@app.get("/get")
def get_messages(query: GetReq):
    args = QueryArguements(
        keyword=query.keyword,
        before_date=query.before_date,
        after_date=query.after_date,
        channel=query.channel_id,
    )
    return database.get_messages(args)
