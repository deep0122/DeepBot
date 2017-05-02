import discord
import asyncio
import html
import random
import time
from foobar import *

client = discord.Client()
user = discord.User()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



@client.event
async def on_message(message):
    if(message.content.startswith('!question')):
        question = message.content[len('!question '):].strip()
        if(question == ''):
            await client.send_message(message.channel,'Proper Usage: !question [your question]')
        else:
            if(random.randint(0,1) == 0):
                await client.send_message(message.channel,'Yes')
            else:
                await client.send_message(message.channel,'No')
    numofquestions = 10
    if(message.content.startswith('!change')):
        temp = message.content.split()
        if temp[1] == "numofquestions":
            if message.author.name == "Deep":
                numofquestions = temp[2]

    if(message.content.startswith('!grouptrivia')):
        print("Group Active")
        temp = message.content[len('!grouptrivia '):].strip()
        playerlist = temp.split()
        dicts = {}
        dict3 = []
        for i in playerlist:
            playerusername = i
            playerusername = playerusername[len('<@'):].strip()
            playerusername = playerusername[:-1]
            print(playerusername)
            dicts[playerusername] = 0

        difflevel = None
        category = None
        getnewquestions(numofquestions,difflevel,category)
        questioncount = 0
        loadfile()
        while(questioncount < numofquestions):
            gqsts = getGroupQuest(questioncount,numofquestions)
            await client.send_message(message.channel,gqsts)
            answerindex = getAns(questioncount)
            dict2 = {}
            print("answer index: " + str(answerindex))
            answer = getAnswer(questioncount)
            time.sleep(2)
            while(True):
                input1 = await client.wait_for_message(timeout=None,author=None)
                if(input1.content == "!trivia end"):
                    await client.send_message(message.channel, 'Group Trivia Ended!')
                    return
                if len(input1.content) == 1:
                    dict2[input1.author.id] = input1.content
                    dict3.append(input1.author.name)
                if len(dict2) >= len(dicts):
                    break
            await client.send_message(message.channel,"Correct answer: " + str(answerindex) + ": " + answer)
            for z in dict2:
                if(int(dict2[z]) == answerindex):
                    #if dicts[z] is not None:
                    dicts[z] += 1
                        #await client.send_message(message.channel,"Correct: " + z)
            questioncount += 1
        await client.send_message(message.channel,"Final scores: ")
        count = 0
        for i in dicts:
            await client.send_message(message.channel,dict3[count] + ": " + str(dicts[i]) + "/" + str(numofquestions))
            count += 1
        closefile()
        print("Group Inactive")


    if(message.content.startswith('!trivia')):
        command = message.content.split()[1]
        if(command == 'help'):
            await client.send_message(message.channel,'```!trivia start\n\t-Starts trivia game with default settings\n\n!trivia start [number of questions] [difficulty level] [category]\n\t[number of questions]: Enter a number (MAX: 100)\n\t[difficulty level]: Enter "easy","medium","hard"\n\t\[category]: anime animals cartoon general geography history videogames boardgames mythology gadgets art comics politics\n\tExample: !trivia start 25 hard history\n\n!grouptrivia [usernames seperated by commas]\n\t-Starts a group trivia game with default settings\n\tExample: !grouptrivia Deep,Wumbo,Yung Guac,Wilkaitty```')

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
                difflevel = "medium";

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
                    guess = await client.wait_for_message(timeout=None, author=message.author)
                    if(guess.content == "!trivia end"):
                        await client.send_message(message.channel, 'Trivia Ended!')
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
