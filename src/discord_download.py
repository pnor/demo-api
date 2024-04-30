#!/usr/bin/env python3

"""
Handles the downloading of discord messages using `discord-chat-exporter` and parsing them
"""


from typing import List, Dict, Any
import datetime
import subprocess
import json
import dateutil
import os

from .type_aliases import ChannelId, Date, Filename, UserToken
from .models import Message


def _run_discord_export_chat_cmd(
    user_token: UserToken, channel_id: ChannelId, destination_file: Filename
) -> Filename:
    time_to_export_after = datetime.datetime.today() - datetime.timedelta(days=7)
    time_as_string = time_to_export_after.strftime("%m/%d/%Y %H:%M")

    subprocess.run(
        [
            "discord-chat-exporter-cli",
            "export",
            "--token",
            user_token,
            "--channel",
            str(channel_id),
            "--output",
            destination_file,
            "--after",
            "{}".format(time_as_string),
            "-f",
            "Json",
        ]
    )

    return destination_file


def _create_messages_from_json(msg_dict: Dict[str, Any]) -> List[Message]:
    messages: List[Message] = []

    channel_id: int = int(msg_dict["channel"]["id"])
    channel_name: str = msg_dict["channel"]["name"]

    for msg in msg_dict["messages"]:
        msg_id: int = int(msg["id"])
        msg_content: str = msg["content"]
        author_name: str = msg["author"]["name"]

        msg_timestamp_str: str = msg["timestamp"]
        msg_timestamp: Date = dateutil.parser.parse(msg_timestamp_str)

        messages.append(
            Message(
                author_name=author_name,
                content=msg_content,
                message_id=msg_id,
                channel_id=channel_id,
                channel_name=channel_name,
                message_timestamp=msg_timestamp,
            )
        )

    return messages


# ===== "Public" functions ===============


def get_messages_from_last_7_days(
    user_token: UserToken, channel_id: ChannelId
) -> List[Message]:
    """
    Gets the messages from `channel_id` from the last 7 days as a list
    """

    # run the cmd to download into the file
    DISCORD_CMD_DOWNLOAD_FILE_NAME = "discord_download.json"

    if os.path.exists(DISCORD_CMD_DOWNLOAD_FILE_NAME):
        os.remove(DISCORD_CMD_DOWNLOAD_FILE_NAME)

    file_with_json = _run_discord_export_chat_cmd(
        user_token, channel_id, DISCORD_CMD_DOWNLOAD_FILE_NAME
    )

    if not os.path.exists(file_with_json):
        raise RuntimeError("Unable to create file with discord output")

    with open(file_with_json) as file:
        discord_json = json.load(file)

    # parse the file to get the json in memory
    messages = _create_messages_from_json(discord_json)

    return messages
