import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
random.seed(10)

lemmatizer = WordNetLemmatizer() # Create an instance of the WordNetLemmatizer class
intents = json.loads(open('intents_spanish.json', 'r', encoding='utf-8').read())


def clean_up_sentence(sentence): # Create a function to clean up the user's input
    sentence_words = nltk.word_tokenize(sentence) # Tokenize the user's input
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words # Return the cleaned up sentence

def bag_of_words(sentence,words): # Create a function to create a bag of words from the user's input 
    sentence_words = clean_up_sentence(sentence) # Clean up the user's input
    bag = [0] * len(words) # Create a list of os with the length of the words list
    for w in sentence_words: # Loop through the words in the user's input 
        for i, word in enumerate(words): # Loop through the words list 1 # Set the value of the word in the bag to 1
            if word == w: # If the word is in the words 
                bag[i]=1
    return np.array(bag) # Return the bag of words

def predict_class(sentence,model_path):
    model = load_model(model_path)
    pkl=(model_path.split('_'))
    pkl.pop()
    pkl="".join(pkl)
    words=pkl+'_'+'words.pkl'
    classes=pkl+'_'+'classes.pkl'
    print(words,classes)
    words = pickle.load(open(words, 'rb')) # Load the words.pkl file
    classes = pickle.load(open(classes, 'rb')) # Load the classes.pkl file

    bow = bag_of_words(sentence,words) # Create a bag of words from the user's input
    res = model.predict(np.array([bow])) [0] # Predict the class of the user's input
    ERROR_THRESHOLD = 0.25 # Set the error threshold to 0.25. Umbral de error, 25% d
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD] # Create a
    results.sort(key=lambda x: x[1], reverse=True) # Sort the list of results by the
    return_list = [] # Create an empty list
    for r in results: # Loop through the results
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])}) #
    print(return_list)
    return return_list # Return the list


def get_response(intents_list, intents_json,model_path):
    tag = intents_list[0]['intent'] # Get the tag of the intent
    list_of_intents = intents_json['intents'] # Get the list of intents
    print("\n\n\n\n\n   \n\n\n\n\n",model_path,"\n\n\n\n\n  \n\n\n\n\n")
    if model_path=="modelos/chatbot_model.h5":
        for i in list_of_intents: # Loop through the list of intents
            if i['tag'] == tag: # If the tag is equal to the tag of the intent
                print(i)
                result = random.choice(i['responses']) # Get a random response from the 
                break # Break out of the loop
    else:
        print("\n\n\n\n\n  sub intents  \n\n\n\n\n")
        clase=(model_path.split('_'))
        print("primera versión de clase:                      ",clase)
        clase.pop()
        print("segunda versión de clase:                      ",clase)
        clase="".join(clase)
        clase=(clase.split('/'))
        clase.pop(0)
        clase="".join(clase)
        print("clase:                         ",clase)
        for i in list_of_intents: # Loop through the list of intents
            print(i)
            if i['tag'] == clase:
                print(clase)
                print("\n\n\n\n\n  pasa  \n\n\n\n\n")
                for j in i['sub_intents']:
                    if j['tag'] == tag: # If the tag is equal to the tag of the intent
                        print(j)
                        print("\n\n\n\n\n  tag correcto  \n\n\n\n\n")
                        result = random.choice(j['responses']) # Get a random response from the 
                        break # Break out of the loop
    return result # Return the response
