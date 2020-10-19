#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 16:51:51 2019

@author: ztiger98
"""
# imported libraries 
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import numpy as np
import matplotlib.pyplot as plt

# initialize the analyzer for sentiment analysis
analyzer = SentimentIntensityAnalyzer()


def replace_all(text, to_replace, replacement):
    pattern = '|'.join(to_replace)
    return re.sub(pattern, replacement, text)

# list of urls for text extraction and scoring
urls = ['https://www.usatoday.com/story/news/politics/2019/11/12/poll-whistleblower-identity-trump-impeachment/2572650001/',
        'https://www.usatoday.com/story/news/politics/2019/11/13/live-trump-impeachment-inquiry-updates-public-testimony-begin/2545436001/',
        'https://www.cnn.com/politics/live-news/impeachment-hearing-11-13-19/h_f9ab171e6ec84bfee0c290beec8b9a02?utm_term=video&utm_medium=social&utm_content=2019-11-13T15%3A44%3A06&utm_source=twCNN',
        'https://www.bbc.com/news/world-us-canada-50266957',
        'https://www.businessinsider.com/trump-impeachment-public-hearing-gop-senators-claim-busy-2019-11']

# initialization of variables
sentence = 0;   
positive = 0;   
negative = 0;   
neutral = 0;     
compound = 0;
top_score = 0;
best_score = 0.0;
values = []
summary = []
my_dict = {}

# parses through each url and extracts the text 
for url in urls: 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Pull all text from the article or body class 
    if soup.find('article') is None:
        text = soup.find('body').text
    else: 
        text = soup.find('article').text

    # adding a symbol to the end of the sentences for splitting purposes
    text = text.replace('.', '.&')
    # split text into a list of sentences 
    text = text.split('&')


    # this loop is for categorizing the sentence scores based on their compund
    # score and then adding them to a dictionary as a list of values for each 
    # url key. 
    for sent in text:
        if sent contains(keyword):
            summary.append(sent)
    
    for p in text: 
        #print(p)
        vs = analyzer.polarity_scores(p)    # setting the score 
        sentence = sentence + 1 
        p = p.split(' ')
        print(p)
        top_score = analyzer.polarity_scores(p[0])
        print(top_score.keys())
        if top_score['neu'] == 1.0:
            top_score['neu'] = 0.0
        print(max(top_score.values()))
        print("hi")
        top_score = max(top_score.values())
        polword = p[0]
        for word in p: 
            scores = analyzer.polarity_scores(word)
            if scores['neu'] == 1.0:
                scores['neu'] = 0.0
            word = max(scores.values())
            if (top_score < word):
                top_score = word
        if vs['compound'] >= 0.05: 
            positive = positive + 1
            compound = compound + vs['compound']
  
        elif vs['compound'] <= - 0.05 : 
            negative = negative + 1
            compound = compound + vs['compound']
  
        else : 
            neutral = neutral + 1 
            compound = compound + vs['compound']
        #print(p)
        #print(vs)
            #    print(vs)
    values = (positive, negative, neutral)
    my_dict[url] = values
    
N = 5
positives = []
numbers = []
#orange bar
negatives = []
neutrals = []
count = 1;
ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

# this loop iterates through the dictionary and adds the numbers from each 
# score to one consolidated list 

for a in my_dict:
    for b in my_dict[a]:
        numbers.append(b)

n = 0
# this loop sperates the numbers from the consolidated list into three other
# lists representing the positive, negative, and neutral components of the 
# three-colored bar graph. 

for n in range(len(numbers)):
    tp = numbers[n]
    if n < 3: 
        if n == 0: 
            positives.append(tp)
        elif n == 1:
            negatives.append(tp)
        elif n == 2: 
            neutrals.append(tp)
        elif n == 3: 
            neutrals.append(tp)
    elif n % 3 == 0:
        positives.append(tp)
    elif n > 3 and n % 3 == 1:
        negatives.append(tp)
    elif n > 3 and n % 3 == 2: 
        neutrals.append(tp)

sums = []
# this loop is necessary for creating a list of the sum of the positive and 
# neutral values so that the negative values can be stacked on top of the 
# neutral value. 

for z in range(len(positives)):
    temp = positives[z] + neutrals[z]
    sums.append(temp)
length = len(positives) - 1

# this loop creates the lot points for the graph.
for i in range(length): 
    p1 = plt.bar(ind, positives, width, color='b')
    p2 = plt.bar(ind, neutrals, width, bottom=positives, color='g')
    p3 = plt.bar(ind, negatives, width, bottom=sums, color='r')

# labeling of graph and axis. 
plt.ylabel('Scores')
plt.title('Scores by URL')
plt.xticks(ind, ('URL1', 'URL2', 'URL3', 'URL4', 'URL5'))
plt.yticks(np.arange(0, 1000, 100))
plt.legend((p1[0], p2[0], p3[0]), ('Positive', 'Neutral', 'Negative'))

# show the graph 
plt.show()

# prints out a statement about each url and the number of positive, negative, 
# and neutral sentences. 

for num in range(len(urls)):
    if num < 4:
        print("URL " + str(num) + " has " + str(positives[num]) + " positive sentences, " + str(neutrals[num]) + " neutral sentences, and " + str(negatives[num]) + " negative sentences.")
    else: 
        break
print("These are the sentences that contain the topic of the article: " + summary)
print("The most polarizes word is " + polword + " with a score of " + top_score)