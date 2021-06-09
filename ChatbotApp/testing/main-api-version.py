import json
import pickle
import random
import numpy
from flask import Flask
from flask import request
import nltk
from nltk.stem import LancasterStemmer

from tensorflow.python.keras.models import model_from_yaml

nltk.download('punkt')

stemmer = LancasterStemmer()

with open("datasets.json") as file:
    data = json.load(file)


# mencoba mengambil data dump pickle
with open("chatbot.pickle", "rb") as file:
	words, labels, training, output = pickle.load(file)


# mengambil model chatbot 
yaml_file = open('chatbotmodel.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
chatbotModel = model_from_yaml(loaded_model_yaml)
chatbotModel.load_weights("chatbotmodel.h5")
print("Loaded model from disk")


def bag_of_words(s, words):
	#melakukan tokenisasi kata dan enumerasi kalimat
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


def chatWithBot(inputText):
	#enumerasi dan tokenisasi
    currentText = bag_of_words(inputText, words)
    currentTextArray = [currentText]
    numpyCurrentText = numpy.array(currentTextArray)
	
	#teks tidak dimengerti
    if numpy.all((numpyCurrentText == 0)):
        return "Maaf saya tidak mengerti maksud Anda, tolong coba lagi."

	#melakukan prediksi dengan model yang di load
    result = chatbotModel.predict(numpyCurrentText[0:1])
    result_index = numpy.argmax(result)
    tag = labels[result_index]
	
	#mengambil respons yang paling tepat dan diambil secara acak
    if result[0][result_index] > 0.7:
        for tg in data["datasets"]:
            if tg['tag'] == tag:
                respons = tg['respons']

        return random.choice(respons)
	
	#respons tidak ada yang tepat
    else:
        return "Maaf saya tidak mengerti maksud anda, tolong coba lagi."


app = Flask(__name__)

@app.route('/chat', methods = ['POST'])
def postJsonHandler():
	content = request.get_json()
	return chatWithBot(content["chat"])

app.run(host='0.0.0.0', port= 80)
