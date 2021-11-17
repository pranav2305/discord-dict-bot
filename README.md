# Dictionary Bot 📚

##### -Pranav Agarwal

<br>

## About

A discord dictionary bot that gives the part of speech, definition, examples, origin, phonetics, synonyms and antonyms. This bot can take multiple inputs and gives the output for all the words after the command in a single message. A flask server is created to upload the discord bot on Repl.it and an uptime bot is used to ping the server every 5 minutes to ensure that the server does'nt go to sleep and the discord bot can be used anytime. The bot also checks if the message is more than 2000 (discord text limit) and splits the message and sends it accordingly.
<br>

## Commands

| Command                       | Function                                                       |
| ----------------------------- | -------------------------------------------------------------- |
| **/mean** <word1> <word2> ... | Gives the _part of speech, definition and examples._           |
| **/org** <word1> <word2> ...  | Gives the _origin_ of the words.                               |
| **/phon** <word1> <word2> ... | Gives the _phonetics text and audio_.                          |
| **/syn** <word1> <word2> ...  | Gives the _part of speech and the synonyms_ under them.        |
| **/ant** <word1> <word2> ...  | Gives the _part of speech and the antonyms_ under them.        |
| **/dict** <word1> <word2> ... | Gives the _meaning, origin, phonetics, synonyms and antonyms_. |

<br>

## Samples

1. Command : **/mean hello world**
   ![Output for "/mean hello world"](./images/1.png)
   <br>
2. Command : **/org helLo WorLd**
   ![Output for "/mean hello world"](./images/2.png)
   <br>
3. Command : **/phon i like cars**
   ![Output for "/mean hello world"](./images/3.png)
   <br>
4. Command : **/syn adfe walk rat**
   ![Output for "/mean hello world"](./images/4.png)
   <br>
5. Command : **/ant happy feet**
   ![Output for "/mean hello world"](./images/5.png)
   <br>
6. Command : **/dict riddle me this**
   ![Output for "/mean hello world"](./images/6_1.png)
   ![Output for "/mean hello world"](./images/6_2.png)
   ![Output for "/mean hello world"](./images/6_3.png)
