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


def getMeaning(res_json):
    new_msg = ""
    for index, meaning in enumerate(res_json[0]["meanings"]):
        new_msg += \
            f"{index+1}. ***Part of Speech*** : {meaning['partOfSpeech']}\n"
        new_msg += \
            f"    ***Definition*** : {meaning['definitions'][0]['definition']}\n"
        new_msg += \
            f"    ***Example*** : {meaning['definitions'][0]['example'].replace('hello', '__hello__')}\n\n"
    return new_msg


def getPhonetics(res_json):
    new_msg = ""
    new_msg += f"***Text*** : {res_json[0]['phonetic']}\n"
    new_msg += f"***Audio*** : {res_json[0]['phonetics'][0]['audio']}\n\n"
    return new_msg


def getSynonyms(res_json):
    new_msg = ""
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
            new_msg += \
                f"{index}. ***Part of Speech*** : {meaning['partOfSpeech']}\n"
            new_msg += f"    ***Synonyms*** : "
            for syn in syns:
                new_msg += syn + ", "
            new_msg = new_msg[:-2] + "\n\n"
            index += 1

    if index == 1:
        new_msg += f"***No synonyms found for {res_json[0]['word'].capitalize()}***\n\n"

    return new_msg


def getOrigin(res_json):
    new_msg = ""
    new_msg += f"***Origin*** : {res_json[0]['origin']}\n\n"
    return new_msg


def getAntonyms(res_json):
    index = 1
    new_msg = ""
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
            new_msg += \
                f"{index}. ***Part of Speech*** : {meaning['partOfSpeech']}\n"
            new_msg += f"    ***Antonyms*** : "
            for ant in ants:
                new_msg += ant + ", "
            new_msg = new_msg[:-2] + "\n\n"
            index += 1

    if index == 1:
        new_msg += f"***No antonyms found for {res_json[0]['word'].capitalize()}***\n\n"

    return new_msg


def getData(func, data, msg):
    l = msg.split()
    if not l[1]:
        return "***Please enter atleast 1 word after '/mean'***"
    else:
        final_msg = ""
        for word in l[1:]:
            res = requests.get(DICT_API + word)
            res_json = json.loads(res.text)
            final_msg += f"**Word\t:\t{word.lower().capitalize()}**\n\n**{data}**\n"
            if type(res_json) == dict:
                final_msg += f"***No results for {word}***\n\n"
            else:
                final_msg += getMeaning(res_json)
            final_msg += "----------\n"
        return final_msg


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith("/mean"):
        await message.channel.send(getData(getMeaning, "Meaning", msg))

    if msg.startswith("/phon"):
        await message.channel.send(getData(getPhonetics, "Phonetics", msg))

    if msg.startswith("/syn"):
        await message.channel.send(getData(getSynonyms, "Synonyms", msg))

    if msg.startswith("/ant"):
        await message.channel.send(getData(getAntonyms, "Antonyms", msg))

    if msg.startswith("/org"):
        await message.channel.send(getData(getOrigin, "Origin", msg))

    if msg.startswith("/dict"):
        l = msg.split()
        if not l[1]:
            await message.channel.send("***Please enter atleast 1 word after '/ant'***")
        else:
            final_msg = ""
            for word in l[1:]:
                final_msg += f"**Word\t:\t{word.lower().capitalize()}**\n\n"
                res = requests.get(DICT_API + word)
                res_json = json.loads(res.text)
                if type(res_json) == dict:
                    final_msg += f"***No results for {word}***\n\n"
                else:
                    final_msg += "**Meaning**\n"
                    final_msg += getMeaning(res_json)
                    final_msg += "**Origin**\n"
                    final_msg += getOrigin(res_json)
                    final_msg += "**Phonetics**\n"
                    final_msg += getPhonetics(res_json)
                    final_msg += "**Synonyms**\n"
                    final_msg += getSynonyms(res_json)
                    final_msg += "**Antonyms**\n"
                    final_msg += getAntonyms(res_json)
                final_msg += "----------\n"
            await message.channel.send(final_msg)

    if msg.startswith("/help"):
        final_msg = """

        **Dictionary Menu**
                    -*Pranav Agarwal*

        1. '***/mean*** <word 1> <word 2> ...' - Gives the part of __*speech, definition and examples*__.

        2. '***/org*** <word 1> <word 2> ...'  - Gives the __*origin*__ of the words.

        3. '***/phon*** <word 1> <word 2> ...' - Gives the __*phonetics text and audio*__.

        4. '***/syn*** <word 1> <word 2> ...'  - Gives the __*part of speech and the synonyms*__ under them.

        5. '***/ant*** <word 1> <word 2> ...'  - Gives the __*part of speech and the antonyms*__ under them.

        6. '***/dict*** <word 1> <word 2> ...' - Gives the __*meaning, origin, phonetics, synonyms and antonyms*__.

        ---------

        """
        await message.channel.send(final_msg)

client.run(TOKEN)
