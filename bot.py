import os

import discord
import requests
import json
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DICT_API = "https://api.dictionaryapi.dev/api/v2/entries/en/"

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith("/dict"):
        l = msg.split()
        if not l[1]:
            await message.channel.send("Please enter atleast 1 word after '\dict'")
        else:
            for word in l[1:]:
                res = requests.get(DICT_API + word)
                res_json = json.loads(res.text)
                dict_msg = f"**Word\t:\t{word.lower().capitalize()}**\n\n"
                for index, meaning in enumerate(res_json[0]["meanings"]):
                    dict_msg += \
                        f"{index+1}. ***Part of Speech*** : {meaning['partOfSpeech']}\n"
                    dict_msg += \
                        f"    ***Definition*** : {meaning['definitions'][0]['definition']}\n"
                    dict_msg += \
                        f"    ***Example*** : {meaning['definitions'][0]['example'].replace('hello', '__hello__')}\n\n"

                await message.channel.send(dict_msg)

client.run(TOKEN)
