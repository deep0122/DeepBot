import random
import html
import requests, json
points = 0

def getGroupQuest(questioncount,numofquestions):
	questiontemp = getQuestion(questioncount)
	question = html.unescape(questiontemp)
	answertemp = getAnswer(questioncount)
	global answer
	answer = html.unescape(answertemp)
	arr = getIncorrect(questioncount)
	arr.append(answer)
	random.shuffle(arr)
	global quests
	quests = {}
	for i in range(len(arr)):
		quests[i+1] = html.unescape(arr[i])
	rtn = '**Q:'+ str(questioncount + 1) + '/' + str(numofquestions) + '**\n\n```' + str(question) + '\n\n'
	for key, value in quests.items():
		rtn += str(key) + ': ' + str(value) + '\n'
	return rtn + "```"

def getQuest(questioncount, pointcount, numofquestions):
    question1 = getQuestion(questioncount)
    question = html.unescape(question1)
    category = getCategory(questioncount)
    global answer
    answer1 = getAnswer(questioncount)
    answer = html.unescape(answer1)
    arr = getIncorrect(questioncount)
    arr.append(answer)
    random.shuffle(arr)
    global quests
    quests = {}
    for i in range(len(arr)):
        quests[i+1] = html.unescape(arr[i])
    rtn = 'Q:'+ str(questioncount + 1) + '/' + str(numofquestions) + '\tP:' + str(pointcount) + '\tCategory: ' + str(category) + '\n\n' + str(question) + '\n\n'
    for key, value in quests.items():
        rtn += str(key) + ': ' + str(value) + '\n'
    return rtn

def getAns(questioncount):
    lst = list(quests.values())
    answerindex = lst.index(answer) + 1
    return int(answerindex)

def getnewquestions(numofquestions, difflevel, category):
    website = 'https://www.opentdb.com/api.php?amount=' + str(numofquestions)
    if category is not None:
        if category == 'anime':
            website += '&category=31'
        if category == 'geography':
            website += '&category=22'
        if category == 'cartoon':
            website += '&category=32'
        if category == 'general':
            website += '&category=9'
        if category == 'animals':
            website += '&category=27'
        if category == 'history':
            website += '&category=23'
        if category == 'videogames':
            website += '&category=15'
        if category == 'boardgames':
            website += '&category=16'
        if category == 'mythology':
            website += '&category=20'
        if category == 'gadgets':
            website += '&category=30'
        if category == 'art':
            website += '&category=25'
        if category == 'comics':
            website += '&category=29'
        if category == 'politics':
            website += '&category=24'

    if difflevel is not None:
        if difflevel == 'easy':
            website += '&difficulty=easy'
        if difflevel == 'medium':
            website += '&difficulty=medium'
        if difflevel == 'hard':
            website += '&difficulty=hard'

    print(website)
    result = requests.get(website)
    output = result.json()
    with open('opentdbquestions.json', 'w') as outfile:
        json.dump(output, outfile)

def loadfile():
    global data_file
    with open('opentdbquestions.json','r') as data_file:
        global output
        output = json.load(data_file)

def closefile():
    data_file.close()

def getQuestion(x):
    return(output["results"][x]["question"])

def getCategory(x):
    return(output["results"][x]["category"])

def getAnswer(x):
    return(output["results"][x]["correct_answer"])

def getIncorrect(x):
    return(output["results"][x]["incorrect_answers"])
