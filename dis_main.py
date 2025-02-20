import os
import sys
from datetime import datetime

import discord
import logging
from discord.ext import tasks

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
)

from src import myYoutube
from src import myTwitch
from src import myJson
from src.data_class import LiveData

BOT_TOKEN = os.environ["discord_token"]
CATEGORY_ADMIN = "管理用"
CHANNEL_LOG = "動作ログ"
CHANNEL_REGISTERD_LIVERS = "登録配信者一覧"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
guild = None

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")


@client.event
async def on_ready():
    print("discord bot login")
    get_onlives_loop.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("makechannel"):

        # get guild(server infomation)
        guild = client.guilds[0]
        print(guild)

        cat = await guild.create_category("dhalshim")
        print("create category\n",cat)
        ch = await guild.create_text_channel(name="yoga",category=cat)
        print("create txtch\n",ch)

    await message.channel.send("a")


@tasks.loop(minutes=15)
async def get_onlives_loop():
    print(f"[{datetime.now()}] get_onlives_loop")

    on_lives:LiveData = []
    
    on_lives += myYoutube.get_onlives()
    on_lives += await myTwitch.get_on_lives()

    print(f"-----\non_lives data\n{on_lives}")

    # get guild(server infomation)
    guild = client.guilds[0]

    await remove_channels(on_lives, guild)
    await send_streaming_messages(on_lives, guild)
    await send_admin_messages(on_lives, guild)

async def remove_channels(on_lives, guild:discord.guild):
    livers_list = set([x.liver_name for x in on_lives])
    del_channels = [x for x in guild.text_channels if x.name not in livers_list and x.category.name != CATEGORY_ADMIN]

    if len(del_channels) > 0:
        print(f"-----\nremove text channels")
        for del_channel in del_channels:
            print(del_channel.name)
            await del_channel.delete()


async def send_streaming_messages(on_lives, guild:discord.guild):
    if len(on_lives) == 0:
        return
    
    print(f"-----\nexist text channels\n{guild.text_channels}")

    for on_live in on_lives:
        exist_channels = [x for x in guild.text_channels if on_live.liver_name == x.name]

        for tag in on_live.liver_tags:
            categories = [x for x in guild.categories if x.name in tag]
            for category in categories:
                category_channels = category.channels
                if not on_live.liver_name in [x.name for x in category_channels]:
                    new_channel = await guild.create_text_channel(name=on_live.liver_name, category=category)
                    exist_channels.append(new_channel)
                    print(f"create text channel:{new_channel.name} - {category.name}")
            
        for channel in exist_channels:
            # check is message duplicate
            messages = [message async for message in channel.history(limit=20)]
            if on_live.live_title in [x.content for x in messages]:
                continue

            await channel.send(on_live.live_title)
            await channel.send(on_live.URL)


async def send_admin_messages(on_lives, guild:discord.guild):
    await send_log_messages(on_lives, guild)
    await send_registed_livers(guild)


async def send_log_messages(on_lives, guild:discord.guild):
    livers_list = set([x.liver_name for x in on_lives])
    log_channel = [x for x in guild.text_channels if x.name == CHANNEL_LOG][0]

    if len(livers_list) > 0:
        await log_channel.send(f"[{datetime.now()}]\n配信中の配信者リスト")
        await log_channel.send("\n".join(livers_list))
    else:
        await log_channel.send(f"[{datetime.now()}]\n配信がありませんでした")


async def send_registed_livers(guild:discord.guild):
    livers_name = myJson.get_livers_name()
    registed_livers_channel = [x for x in guild.text_channels if x.name == CHANNEL_REGISTERD_LIVERS][0]

    messages = [message async for message in registed_livers_channel.history(limit=100)]
    await registed_livers_channel.delete_messages(messages)
    await registed_livers_channel.send("\n".join(livers_name))



client.run(BOT_TOKEN, log_handler=handler)