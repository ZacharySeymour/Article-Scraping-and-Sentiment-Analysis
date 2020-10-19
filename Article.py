import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import numpy as np
import matplotlib.pyplot as plt

class Article: 

	def __init__(self, url):
		self.url = url

	def score(self):
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

		# initialize the analyzer for sentiment analysis
		analyzer = SentimentIntensityAnalyzer()
		url = self.url 
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
		for p in text: 
			vs = analyzer.polarity_scores(p)    # setting the score 
			sentence = sentence + 1 
			p = p.split(' ')
			if vs['compound'] >= 0.05: 
				positive = positive + 1
				compound = compound + vs['compound']
			elif vs['compound'] <= - 0.05 : 
				negative = negative + 1
				compound = compound + vs['compound']
			else: 
				neutral = neutral + 1 
				compound = compound + vs['compound']

	        #save values to dictionary 
		values = (positive, negative, neutral)
		my_dict[url] = values
		return my_dict


	def plot(self, dictionary):

		my_dict = dictionary
		N = 1
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

		# this loop creates the plot points for the graph.
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

		# returns a statement about each url and the number of positive, negative, 
		# and neutral sentences. 
		return ("URL " + str(num) + " has " + str(positives[num]) + " positive sentences, " + str(neutrals[num]) + " neutral sentences, and " + str(negatives[num]) + " negative sentences.")


art = Article('https://www.usatoday.com/story/news/politics/2019/11/12/poll-whistleblower-identity-trump-impeachment/2572650001/')
print(art.score())
    