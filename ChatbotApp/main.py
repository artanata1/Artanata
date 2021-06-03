import json
import pickle
import random
import numpy

import nltk
from nltk.stem import LancasterStemmer

from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.models import model_from_yaml

nltk.download('punkt')

stemmer = LancasterStemmer()

with open("datasets.json") as file:
    data = json.load(file)

try:
    with open("chatbot.pickle", "rb") as file:
        words, labels, training, output = pickle.load(file)

except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for dataset in data["datasets"]:
        for quest in dataset["quests"]:
            wrds = nltk.word_tokenize(quest)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(dataset["tag"])

        if dataset["tag"] not in labels:
            labels.append(dataset["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    output_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = output_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("chatbot.pickle", "wb") as file:
        pickle.dump((words, labels, training, output), file)

try:
    yaml_file = open('chatbotmodel.yaml', 'r')
    loaded_model_yaml = yaml_file.read()
    yaml_file.close()
    chatbotModel = model_from_yaml(loaded_model_yaml)
    chatbotModel.load_weights("chatbotmodel.h5")
    print("Loaded model from disk")

except:
    # Make our neural network
    chatbotModel = Sequential()
    chatbotModel.add(Dense(8, input_shape=[len(words)], activation='relu'))
    chatbotModel.add(Dense(len(labels), activation='softmax'))

    # optimize the model
    chatbotModel.compile(loss='categorical_crossentropy',
                         optimizer='adam', metrics=['accuracy'])

    # train the model
    chatbotModel.fit(training, output, epochs=250, batch_size=10)

    # serialize model to yaml and save it to disk
    model_yaml = chatbotModel.to_yaml()
    with open("chatbotmodel.yaml", "w") as y_file:
        y_file.write(model_yaml)

    # serialize weights to HDF5
    chatbotModel.save_weights("chatbotmodel.h5")
    print("Saved model from disk")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


def chatWithBot(inputText):
    currentText = bag_of_words(inputText, words)
    currentTextArray = [currentText]
    numpyCurrentText = numpy.array(currentTextArray)

    if numpy.all((numpyCurrentText == 0)):
        return "Maaf saya tidak mengerti maksud Anda, tolong coba lagi."

    result = chatbotModel.predict(numpyCurrentText[0:1])
    result_index = numpy.argmax(result)
    tag = labels[result_index]

    if result[0][result_index] > 0.7:
        for tg in data["datasets"]:
            if tg['tag'] == tag:
                respons = tg['respons']

        return random.choice(respons)

    else:
        return "Maaf saya tidak mengerti maksud anda, tolong coba lagi."


def chat():
    print("Mulailah untuk chat dengan saya disini. Ketik 'Bye' untuk mengakhiri percakapan.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print(chatWithBot(user_input))
            break

        print(chatWithBot(user_input))


chat()
