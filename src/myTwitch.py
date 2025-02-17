import asyncio
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
import os
import json
from data_class import LiveData

twitch_app_id = os.environ["twitch_app_id"]
twitch_app_secret = os.environ["twitch_app_secret"]

async def get_on_lives():

    json_file = open("./json/streamers.json", 'r', encoding="utf-8_sig")
    livers = json.load(json_file)
    on_lives = []

    twitch = await Twitch(twitch_app_id, twitch_app_secret)

    # check on lives
    for liver in livers["data"]:
        if not liver["twitch"]["display_name"]:
            continue
        
        stream = await first(twitch.get_streams(user_login=liver["twitch"]["display_name"]))
        if stream is not None:
            data = LiveData(liver["name"], stream.title, liver["twitch"]["URL"], liver["tags"])
            on_lives.append(data)

    await twitch.close()

    return on_lives


if __name__ == "__main__":
    asyncio.run(get_on_lives())