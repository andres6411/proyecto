import nltk
from nltk.stem import WordNetLemmatizer 
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense,Dropout
from keras.optimizers import SGD
from keras.optimizers.schedules import ExponentialDecay 
import random

data_file = open('intents_spanish.json', 'r', encoding= 'utf-8').read()
intents = json.loads(data_file)

lemmatizer = WordNetLemmatizer()

words=[]
classes = []
documents = []
ignore_words = ['?', '!']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))