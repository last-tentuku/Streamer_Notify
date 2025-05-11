import asyncio
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
import os
import myJson
import src.data_class as data_class
from src.data_class import LiveData

twitch_app_id = os.environ["twitch_app_id"]
twitch_app_secret = os.environ["twitch_app_secret"]

async def get_on_lives():
    print("twitch get_on_lives start --- ")
    livers = myJson.load_livers()
    on_lives = []

    print("create twitch instance")
    twitch = await Twitch(twitch_app_id, twitch_app_secret)

    # check on lives
    for liver in livers:
        if not liver["twitch"]["display_name"]:
            continue
        
        stream = await first(twitch.get_streams(user_login=liver["twitch"]["display_name"]))
        if stream is not None:
            data = LiveData(liver["name"], stream.title, liver["twitch"]["URL"], liver["tags"])
            data_class.printData(data)
            on_lives.append(data)

    await twitch.close()

    return on_lives


if __name__ == "__main__":
    asyncio.run(get_on_lives())