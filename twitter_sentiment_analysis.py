import tweepy
import sys
import matplotlib.pyplot as plt
import numpy as np
import time
from textblob import TextBlob

consumer_key = 'xxxxxxxxxxx'
consumer_secret = 'xxxxxxx'

access_token = 'xxxxxxxxxxx'
access_token_secret = 'xxxxxxxxxxx'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
now = time.strftime("%c")

names = np.array(['Trump', 'Obama', 'Merkel', 'Putin', 'Jong-un', 'Hitler', 'Castro', 'Hussein', 'Guevara'])
scores = np.zeros(len(names))

def getScores(str):
	public_tweets = api.search(str, lang="en", count=100)
	polarity_sum = 0	
	for tweet in public_tweets:
		#print(tweet.text).encode(sys.stdout.encoding, errors='replace')
		analysis = TextBlob(tweet.text)
		#print(analysis.sentiment.polarity)
		polarity_sum += analysis.sentiment.polarity

	return polarity_sum/len(public_tweets);

count = 0
for n in names:
	score = getScores(n)
	scores[count] = score
	count += 1
	print(score)



n_groups = len(names)
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.55
opacity = 0.8

rects1 = plt.bar(index, scores, bar_width,
                 alpha=opacity,
                 color='b',                 
                 label='Polarity [-1, 1]')


for x in range(0, n_groups):
	scl = scores[x]	
	if scl<0:
		rects1[x].set_color((0.9,0,0))
	else: rects1[x].set_color((0,0,0.9))

rects = ax.patches
for rect,scl in zip(rects,scores):
	height = rect.get_height()
	ax.text(rect.get_x() + rect.get_width()/2, height , round(scl,2), ha='center', va='bottom')


plt.xticks(index , names)
plt.ylim((-0.05,0.25))
plt.hlines(0, 0-bar_width, n_groups, colors='k', linestyles='solid', label='')
plt.ylabel(now)
plt.legend()

plt.tight_layout()
plt.show()
