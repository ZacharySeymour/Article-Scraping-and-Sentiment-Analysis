#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 16:12:40 2019

@author: ztiger98
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

pos_count = 0
pos_correct = 0

with open("texty.txt","r") as f:
    for line in f.read().split('\n'):
        vs = analyzer.polarity_scores(line)
        if not vs['neg'] > 0.1:
            if vs['pos']-vs['neg'] > 0:
                pos_correct += 1
            pos_count +=1


neg_count = 0
neg_correct = 0

with open("testy2.txt","r") as f:
    for line in f.read().split('\n'):
        vs = analyzer.polarity_scores(line)
        if not vs['pos'] > 0.1:
            if vs['pos']-vs['neg'] <= 0:
                neg_correct += 1
            neg_count +=1

print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_count*100.0, pos_count))
print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_count*100.0, neg_count))