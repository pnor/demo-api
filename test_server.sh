#!/usr/bin/env sh

DISCORD_TOKEN="noterealtoken"

SERVER_URL="http://127.0.0.1:8000"

CMD="$1"
shift

# Get all
# Get keyword
# Get after date
# Get before date

case "$CMD" in
    "hello")
        echo "read root endpoint; hello world"
        curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET "$SERVER_URL"

        ;;
    "store")
        echo "Running store"
        # TODO rm
        echo "Channel = $1"
        data='{"user_token": "'$DISCORD_TOKEN'", "channel": "'$1'"}'
        curl -H "Accept: application/json" -H "Content-Type: application/json" --data "$data" "$SERVER_URL/download"
    ;;
    "get")
        echo "get [all] messages"
        data='{"user_token" : "'$DISCORD_TOKEN'"}'
        curl -i -H "Accept: application/json" -H "Content-Type: application/json" --data "$data"  -X GET "$SERVER_URL/get"
    ;;
    "get-key")
        echo "get messages with keyword, $1"
        data='{"user_token" : "'$DISCORD_TOKEN'", "keyword": "'$1'"}'
        curl -i -H "Accept: application/json" -H "Content-Type: application/json" --data "$data"  -X GET "$SERVER_URL/get"
    ;;
    "get-after")
        echo "get messages after date : $1"
        data='{"user_token": "'$DISCORD_TOKEN'", "after_date": "'$1'"}'
        curl -i -H "Accept: application/json" -H "Content-Type: application/json" --data "$data" -X GET "$SERVER_URL/get"
    ;;
    "get-before")
        echo "get messages before date : $1"
        data='{"user_token": "'$DISCORD_TOKEN'", "before_date": "'$1'"}'
        curl -i -H "Accept: application/json" -H "Content-Type: application/json" --data "$data" -X GET "$SERVER_URL/get"
    ;;
    "get-channel")
        echo "get messages from channel: $1"
        data='{"user_token": "'$DISCORD_TOKEN'", "channel_id": "'$1'"}'
        curl -i -H "Accept: application/json" -H "Content-Type: application/json" --data "$data" -X GET "$SERVER_URL/get"
    ;;
    *)
        echo "invalid command"
    ;;
esac
