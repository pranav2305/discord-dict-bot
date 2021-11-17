import os

import discord
import requests
import json
from dotenv import load_dotenv
from server import server

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DICT_API = "https://api.dictionaryapi.dev/api/v2/entries/en/"

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# Function to get all the meanings from the json object


def getMeaning(res_json):
    new_msg = ""
    for index, meaning in enumerate(res_json[0]["meanings"]):
        new_msg += \
            f"{index+1}. ***Part of Speech*** : {meaning['partOfSpeech']}\n"
        new_msg += \
            f"    ***Definition*** : {meaning['definitions'][0]['definition']}\n"
        replaceText = f"__*{res_json[0]['word']}*__"
        if "example" in meaning['definitions'][0]:
            new_msg += \
                f"    ***Example*** : {meaning['definitions'][0]['example'].replace(res_json[0]['word'], replaceText)}\n\n"
    return new_msg

# Function to get phonetics from the json object


def getPhonetics(res_json):
    new_msg = ""
    new_msg += f"***Text*** : {res_json[0]['phonetic']}\n"
    new_msg += f"***Audio*** : {res_json[0]['phonetics'][0]['audio']}\n\n"
    return new_msg

# Function to get synonyms from the json object


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

# Function to get the origin from the json object


def getOrigin(res_json):
    new_msg = ""
    if "origin" in res_json[0]:
        new_msg += f"***Origin*** : {res_json[0]['origin']}\n\n"
    else:
        new_msg = f"***No origin found for {res_json[0]['word'].capitalize()}***\n\n"
    return new_msg

# Function to get antonyms from the json object


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

# Function to get all the data from the json object


def getData(func, data, msg):
    l = msg.split()
    if not l[1]:
        return ["***Please enter atleast 1 word after '/mean'***"]
    else:
        msgs = []
        for word in l[1:]:
            res = requests.get(DICT_API + word)
            res_json = json.loads(res.text)
            final_msg = f"**Word\t:\t{word.lower().capitalize()}**\n\n**{data}**\n"
            if type(res_json) == dict:
                final_msg += f"***No results for {word}***\n\n"
            else:
                final_msg += func(res_json)
            final_msg += "----------\n"
            if not msgs:
                msgs.append(final_msg)
            elif len(final_msg) + len(msgs[-1]) < 2000:
                msgs[-1] += final_msg
            else:
                msgs.append(final_msg)
        return msgs


@ client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith("/mean"):
        for m in getData(getMeaning, "Meaning", msg):
            await message.channel.send(m)

    if msg.startswith("/phon"):
        for m in getData(getMeaning, "Meaning", msg):
            await message.channel.send(m)

    if msg.startswith("/syn"):
        for m in getData(getMeaning, "Meaning", msg):
            await message.channel.send(m)

    if msg.startswith("/ant"):
        for m in getData(getMeaning, "Meaning", msg):
            await message.channel.send(m)

    if msg.startswith("/org"):
        for m in getData(getMeaning, "Meaning", msg):
            await message.channel.send(m)

    if msg.startswith("/dict"):
        l = msg.split()
        if not l[1]:
            await message.channel.send("***Please enter atleast 1 word after '/ant'***")
        else:
            msgs = []
            for word in l[1:]:
                final_msg = f"**Word\t:\t{word.lower().capitalize()}**\n\n"
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
                if not msgs:
                    msgs.append(final_msg)
                elif len(final_msg) + len(msgs[-1]) < 2000:
                    msgs[-1] += final_msg
                else:
                    msgs.append(final_msg)
            for m in msgs:
                await message.channel.send(m)

    if msg.startswith("/help"):
        final_msg = """

        **Dictionary Menu**
                    -*Pranav Agarwal*

        1. '***/mean*** <word1> <word2> ...' - Gives the __*part of speech, definition and examples*__.

        2. '***/org*** <word1> <word2> ...'  - Gives the __*origin*__ of the words.

        3. '***/phon*** <word1> <word2> ...' - Gives the __*phonetics text and audio*__.

        4. '***/syn*** <word1> <word2> ...'  - Gives the __*part of speech and the synonyms*__ under them.

        5. '***/ant*** <word1> <word2> ...'  - Gives the __*part of speech and the antonyms*__ under them.

        6. '***/dict*** <word1> <word2> ...' - Gives the __*meaning, origin, phonetics, synonyms and antonyms*__.

        ---------

        """
        await message.channel.send(final_msg)

server()
client.run(TOKEN)
