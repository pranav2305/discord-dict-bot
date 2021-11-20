import os

import discord
import requests
import json
from dotenv import load_dotenv
from server import server

load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']
DICT_API = "https://api.dictionaryapi.dev/api/v2/entries/en/"
SLANG_API = "https://api.urbandictionary.com/v0/define?term="

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# Function to get short meanings from the json object


def getShortMeaning(res_json):
    new_msg = ""
    pos = []
    index = 1
    for res_j in res_json:
        for meaning in res_j["meanings"]:
            if meaning["partOfSpeech"] not in pos:
                new_msg += \
                    f"{index}. ***Part of Speech*** : {meaning['partOfSpeech']}\n"
                index += 1
                pos.append(meaning['partOfSpeech'])
                new_msg += \
                    f"    ***Definition*** : {meaning['definitions'][0]['definition']}"
                replaceText = f"__*{res_json[0]['word']}*__"
                if "example" in meaning['definitions'][0]:
                    new_msg += \
                        f"\n    ***Example*** : {meaning['definitions'][0]['example'].replace(res_json[0]['word'], replaceText)}"
                new_msg += "\n\n"
    return new_msg

# Function to get all the meanings from the json object


def getLongMeaning(res_json):
    new_msg = ""
    pos = []
    index = 1
    for res_j in res_json:
        for meaning in res_j["meanings"]:
            if meaning["partOfSpeech"] not in pos:
                new_msg += \
                    f"{index}. ***Part of Speech*** : {meaning['partOfSpeech']}\n"
                index += 1
                pos.append(meaning['partOfSpeech'])
                for i, defn in enumerate(meaning['definitions']):
                    new_msg += \
                        f"    ({chr(ord('a') + i)}.) ***Definition*** : {defn['definition']}"
                    replaceText = f"__*{res_json[0]['word']}*__"
                    if "example" in meaning['definitions'][0]:
                        new_msg += \
                            f"\n          ***Example*** : {meaning['definitions'][0]['example'].replace(res_json[0]['word'], replaceText)}"
                    new_msg += "\n\n"
    return new_msg

# Function to get phonetics from the json object


def getPhonetics(res_json):
    new_msg = ""
    if "phonetic" in res_json[0]:
        new_msg += f"***Text*** : {res_json[0]['phonetic']}\n"
        new_msg += f"***Audio*** : {res_json[0]['phonetics'][0]['audio']}\n\n"
    else:
        new_msg += f"***No phonetics found for {res_json[0]['word'].capitalize()}***\n\n"
    return new_msg

# Function to get synonyms from the json object


def getSynonyms(res_json):
    new_msg = ""
    index = 1
    pos = []
    for res_j in res_json:
        for meaning in res_j["meanings"]:
            if meaning["partOfSpeech"] not in pos:
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
                    pos.append(meaning['partOfSpeech'])
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
    pos = []
    for res_j in res_json:
        for meaning in res_j["meanings"]:
            if meaning["partOfSpeech"] not in pos:
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
                    pos.append(meaning['partOfSpeech'])
                    new_msg += f"    ***Antonyms*** : "
                    for ant in ants:
                        new_msg += ant + ", "
                    new_msg = new_msg[:-2] + "\n\n"
                    index += 1

    if index == 1:
        new_msg += f"***No antonyms found for {res_json[0]['word'].capitalize()}***\n\n"

    return new_msg

# Function to get meaning and examples from json object


def getSlang(res_json):
    new_msg = ""
    if res_json["list"]:
        defn = res_json["list"][0]
        new_msg += \
            f"***Definition*** : \n{defn['definition'].replace('[', '').replace(']', '')}\n"
        replaceText = f"__*{defn['word']}*__"
        new_msg += f"***Example*** : \n{defn['example'].replace('[', '').replace(']', '').replace(defn['word'], replaceText).replace(defn['word'].upper(), replaceText.upper()).replace(defn['word'].capitalize(), replaceText)}\n\n"

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
            if type(res_json) == dict:
                final_msg = f"**Word\t:\t{word.lower().capitalize()}**\n\n**{data}**\n"
                final_msg += f"***No results for {word}***\n\n"
            else:
                final_msg = f"**Word\t:\t{res_json[0]['word'].lower().capitalize()}**\n\n**{data}**\n"
                final_msg += func(res_json)
            final_msg += "----------\n"
            if not msgs:
                msgs.append(final_msg)
            elif len(final_msg) + len(msgs[-1]) < 2000:
                msgs[-1] += final_msg
            else:
                msgs.append(final_msg)
        return msgs


def getMenu():
    return """

**Dictionary Menu**
            -*Pranav Agarwal*

1. '***/mean*** <word1> <word2> ...' - Gives the __*part of speech, definition and examples*__.

2. '***/org*** <word1> <word2> ...' - Gives the __*origin*__ of the words.

3. '***/phon*** <word1> <word2> ...' - Gives the __*phonetics text and audio*__.

4. '***/syn*** <word1> <word2> ...' - Gives the __*part of speech and the synonyms*__ under them.

5. '***/ant*** <word1> <word2> ...' - Gives the __*part of speech and the antonyms*__ under them.

6. '***/dict*** <word1> <word2> ...' - Gives the __*short meaning, origin, phonetics, synonyms and antonyms*__.

7. '***/slang*** <word1> <word2> ...' - Gives the __*meaning and example*__ for slangs.

8. '***/menu***' - Gives the __*menu*__ for the dictionary bot.

---------

"""


@ client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith("/mean"):
        for m in getData(getLongMeaning, "Meaning", msg):
            await message.channel.send(m)

    if msg.startswith("/phon"):
        for m in getData(getPhonetics, "Phonetics", msg):
            await message.channel.send(m)

    if msg.startswith("/syn"):
        for m in getData(getSynonyms, "Synonyms", msg):
            await message.channel.send(m)

    if msg.startswith("/ant"):
        for m in getData(getAntonyms, "Antonyms", msg):
            await message.channel.send(m)

    if msg.startswith("/org"):
        for m in getData(getOrigin, "Origin", msg):
            await message.channel.send(m)

    if msg.startswith("/dict"):
        l = msg.split()
        if not l[1]:
            await message.channel.send("***Please enter atleast 1 word after '/ant'***")
        else:
            msgs = []
            for word in l[1:]:
                res = requests.get(DICT_API + word)
                res_json = json.loads(res.text)
                if type(res_json) == dict:
                    final_msg = f"**Word\t:\t{word.lower().capitalize()}**\n\n"
                    final_msg += f"***No results for {word}***\n\n"
                else:
                    final_msg = f"**Word\t:\t{res_json[0]['word'].lower().capitalize()}**\n\n"
                    final_msg += "**Meaning**\n"
                    final_msg += getShortMeaning(res_json)
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

    if msg.startswith("/slang"):
        l = msg.split()
        if not l[1]:
            return ["***Please enter atleast 1 word after '/slang'***"]
        else:
            msgs = []
            for word in l[1:]:
                res = requests.get(SLANG_API + word)
                res_json = json.loads(res.text)
                if "list" in res_json and res_json['list']:
                    final_msg = f"**Word\t:\t{res_json['list'][0]['word'].lower().capitalize()}**\n\n"
                    final_msg += getSlang(res_json)
                else:
                    final_msg = f"**Word\t:\t{word.lower().capitalize()}**\n\n"
                    final_msg += f"***No results for {word}***\n\n"
                final_msg += "----------\n\n"
                if not msgs:
                    msgs.append(final_msg)
                elif len(final_msg) + len(msgs[-1]) < 2000:
                    msgs[-1] += final_msg
                else:
                    msgs.append(final_msg)
            for m in msgs:
                await message.channel.send(m)

    if msg.startswith("/menu"):
        await message.channel.send(getMenu())


@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(getMenu())
            break

server()
client.run(TOKEN)
