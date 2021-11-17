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
            await message.channel.send("***Please enter atleast 1 word after '/dict'***")
        else:
            for word in l[1:]:
                res = requests.get(DICT_API + word)
                res_json = json.loads(res.text)
                dict_msg = f"**Word\t:\t{word.lower().capitalize()}**\n\n**Meanings**\n"
                for index, meaning in enumerate(res_json[0]["meanings"]):
                    dict_msg += \
                        f"{index+1}. ***Part of Speech*** : {meaning['partOfSpeech']}\n"
                    dict_msg += \
                        f"    ***Definition*** : {meaning['definitions'][0]['definition']}\n"
                    dict_msg += \
                        f"    ***Example*** : {meaning['definitions'][0]['example'].replace('hello', '__hello__')}\n\n"

                await message.channel.send(dict_msg)

    if msg.startswith("/phon"):
        l = msg.split()
        if not l[1]:
            await message.channel.send("***Please enter atleast 1 word after '/phon'***")
        else:
            for word in l[1:]:
                res = requests.get(DICT_API + word)
                res_json = json.loads(res.text)
                dict_msg = f"**Word\t:\t{word.lower().capitalize()}**\n\n**Phonetics**\n"
                dict_msg += f"***Text*** : {res_json[0]['phonetic']}\n"
                dict_msg += f"***Audio*** : {res_json[0]['phonetics'][0]['audio']}\n"
                await message.channel.send(dict_msg)

    if msg.startswith("/syn"):
        l = msg.split()
        if not l[1]:
            await message.channel.send("***Please enter atleast 1 word after '/syn'***")
        else:
            for word in l[1:]:
                res = requests.get(DICT_API + word)
                res_json = json.loads(res.text)
                dict_msg = f"**Word\t:\t{word.lower().capitalize()}**\n\n**Synonyms**\n"
                index = 1
                for meaning in res_json[0]["meanings"]:
                    syns = []
                    for defns in meaning["definitions"]:
                        count = 0
                        if defns["synonyms"]:
                            for syn in defns["synonyms"]:
                                syns.append(syn)
                                count += 1
                                if count == 2:
                                    break
                    if syns:
                        dict_msg += \
                            f"{index}. ***Part of Speech*** : {meaning['partOfSpeech']}\n"
                        dict_msg += f"    ***Synonyms*** : "
                        for syn in syns:
                            dict_msg += syn + ", "
                        dict_msg = dict_msg[:-2] + "\n\n"
                        index += 1

                if index == 1:
                    dict_msg += f"***No synonyms found for {word}***"

                await message.channel.send(dict_msg)

    if msg.startswith("/ant"):
        l = msg.split()
        if not l[1]:
            await message.channel.send("***Please enter atleast 1 word after '/ant'***")
        else:
            for word in l[1:]:
                res = requests.get(DICT_API + word)
                res_json = json.loads(res.text)
                dict_msg = f"**Word\t:\t{word.lower().capitalize()}**\n\n**Antonyms**\n"
                index = 1
                for meaning in res_json[0]["meanings"]:
                    ants = []
                    for defns in meaning["definitions"]:
                        count = 0
                        if defns["antonyms"]:
                            for ant in defns["antonyms"]:
                                ants.append(ant)
                                count += 1
                                if count == 2:
                                    break
                    if ants:
                        dict_msg += \
                            f"{index}. ***Part of Speech*** : {meaning['partOfSpeech']}\n"
                        dict_msg += f"    ***Antonyms*** : "
                        for ant in ants:
                            dict_msg += ant + ", "
                        dict_msg = dict_msg[:-2] + "\n\n"
                        index += 1

                if index == 1:
                    dict_msg += f"***No antonyms found for {word}***"

                await message.channel.send(dict_msg)

client.run(TOKEN)
