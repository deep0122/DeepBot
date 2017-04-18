import discord
import asyncio
import html
from foobar import *

client = discord.Client()
client.change_presence(game="NUT",status=None,afk=False)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if(message.content.startswith('!trivia')):
        command = message.content.split()[1]
        if(command == 'help'):
            await client.send_message(message.channel,'1. !trivia start\n\t-Starts trivia game with default settings')
            await client.send_message(message.channel,'\n2. !trivia start [number of questions] [difficulty level] [category]\n\t[number of questions]: Enter a number (MAX: 100)\n\t[difficulty level]: Enter "easy","medium","hard"\n\t\[category]: anime animals cartoon general geography history videogames boardgames mythology gadgets art comics politics\n\tExample: !trivia start 25 hard history')

        if(command == 'start'):
            print('Active')
            inputarray = message.content.split()
            try:
                numofquestions = int(inputarray[2])
            except:
                numofquestions = 20

            try:
                difflevel = inputarray[3]
            except:
                difflevel = None

            try:
                category = inputarray[4]
            except:
                category = None

            getnewquestions(numofquestions,difflevel,category)
            questioncount = 0
            points = 0
            loadfile()
            while(questioncount < numofquestions):
                gqst = getQuest(questioncount, points, numofquestions)
                await client.send_message(message.channel, str(gqst))
                answerindex = getAns(questioncount)
                answer = getAnswer(questioncount)
                while(True):
                    guess = await client.wait_for_message(timeout=180, author=message.author)
                    if(guess.content == "!trivia end"):
                        await client.send_message(message.channel, 'Game Ended!')
                        return
                    else:
                        try:
                            if(int(guess.content) == answerindex):
                                await client.send_message(message.channel, 'Correct!')
                                points += 1
                                break
                            else:
                                await client.send_message(message.channel, 'Incorrect!\tCorrect Answer:\t' + str(answerindex) + ': ' + html.unescape(str(answer)))
                                break
                        except:
                            await client.send_message(message.channel,'Incorrect Input. Try Again')

                questioncount += 1

            closefile()
            await client.send_message(message.channel, 'Score: ' + str(points) + '/' + str(numofquestions))
            print('Inactive')

    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

client.run('TOKEN_ID')
