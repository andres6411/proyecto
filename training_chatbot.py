import nltk
nltk.download('punkt_tab')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
from keras.optimizers.schedules import ExponentialDecay
import random

data_file = open('intents_spanish.json', 'r', encoding="utf-8").read()
intents = json.loads(data_file)

lemmatizer = WordNetLemmatizer()

words = []
classes = []
documents = []
ignore_words = ['?', '!']

# Recorre cada intención y sus patrones en el archivo JSON

for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokeniza las palabras en cada patrón y las agrega a la lista de palabras
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        # Agrega el par (patrón, etiqueta) a la lista de documentos
        documents.append((w, intent['tag']))
        # Si la etiqueta no está en la lista de clases, la agrega
        if intent['tag'] not in classes: 
            classes.append(intent['tag'])


def train(words,classes,documents,ignore_words,model_name):

    # Lematiza las palabras y las convierte en minúsculas, excluyendo las palabras ignoradas
    words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
    words = sorted(list(set(words)))
    classes = sorted(list(set(classes)))

    # Guarda las listas de palabras y clases en archivos pickle 
    pkl=(model_name.split('_'))
    pkl.pop()
    pkl="".join(pkl)
    words_pkl=pkl+'_'+'words.pkl'
    classes_pkl=pkl+'_'+'classes.pkl'
    pickle.dump(words,open(words_pkl,'wb'))
    pickle.dump(classes, open(classes_pkl,'wb'))

    training = []
    output_empty = [0] * len(classes)

    # Crea el conjunto de entrenamiento
    for doc in documents:
        bag = []
        pattern_words = doc[0]
        pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
        for word in words:
            # Crea una bolsa de palabras binaria para cada patrón
            bag.append(1) if word in pattern_words else bag.append(0)
        output_row = list(output_empty)
        # Crea un vector de salida con un 1 en la posición correspondiente a la etiqueta de la intención
        output_row[classes.index(doc[1])] = 1
        training.append([bag, output_row])

    # Mezcla aleatoriamente el conjunto de entrenamiento
    random.shuffle(training)

    # Divide el conjunto de entrenamiento en características (train_x) y etiquetas (train_y)
    train_x = [row[0] for row in training]
    train_y = [row[1] for row in training]

    train_x = np.array(train_x)
    train_y = np.array(train_y)

    # Crea el modelo de red neuronal
    model = Sequential()
    model.add(Dense (128, input_shape=(len(train_x[0]),), activation= 'relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation='softmax'))

    # Configura el optimizador con una tasa de aprendizaje exponencialmente decreciente
    lr_schedule = ExponentialDecay(
        initial_learning_rate=0.01,
        decay_steps=10000,
        decay_rate=0.9)
    sgd = SGD(learning_rate=lr_schedule, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    # Entrena el modelo con el conjunto de entrenamiento
    hist = model.fit(np.array (train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

    # Guarda el modelo entrenado en un archivo h5
    model.save(model_name, hist)

    print("model created",model_name)

train(words,classes,documents,ignore_words,"modelos/chatbot_model.h5")


for intent in intents['intents']:
    if 'sub_intents' in intent:
        words = []
        classes = []
        documents = []
        ignore_words = ['?', '!']        
        model_name="modelos/"+intent['tag']+"_model.h5"
        for sub_intent in intent["sub_intents"]:
            for pattern in sub_intent['patterns']:
                # Tokeniza las palabras en cada patrón y las agrega a la lista de palabras
                w = nltk.word_tokenize(pattern)
                words.extend(w)
                # Agrega el par (patrón, etiqueta) a la lista de documentos
                documents.append((w, sub_intent['tag']))
                # Si la etiqueta no está en la lista de clases, la agrega
                if sub_intent['tag'] not in classes: 
                    classes.append(sub_intent['tag'])
        train(words,classes,documents,ignore_words,model_name)