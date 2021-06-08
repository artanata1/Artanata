import json
import pickle
import random
import numpy
from flask import Flask
from flask import request
import nltk
from nltk.stem import LancasterStemmer

model = None
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
	global model
	#enumerasi dan tokenisasi
	currentText = bag_of_words(inputText, words)
	currentTextArray = [currentText]
	numpyCurrentText = numpy.array(currentTextArray)
	
	#teks tidak dimengerti
	if numpy.all((numpyCurrentText == 0)):
		return "Maaf saya tidak mengerti maksud Anda, tolong coba lagi."

	#melakukan prediksi dengan model yang di load
	result = model.predict(numpyCurrentText[0:1])
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

def download_blob(bucket_name, source_blob_name, destination_file_name):
	"""Downloads a blob from the bucket."""
	storage_client = storage.Client()
	bucket = storage_client.get_bucket(bucket_name)
	blob = bucket.blob(source_blob_name)

	blob.download_to_filename(destination_file_name)

	print('Blob {} downloaded to {}.'.format(
		source_blob_name,
		destination_file_name))

def handler(request):
	global model

	# Model load which only happens during cold starts
	if model is None:
		
		#dataset datasets.json
		download_blob(bucket, 'datasets.json', '/tmp/datasets.json')
		with open("datasets.json") as file:
			data = json.load(file)
		print("loaded dataset")

		#pickle chatbot.pickle
		download_blob(bucket, 'chatbot.pickle', '/tmp/chatbot.pickle')
		with open("/tmp/chatbot.pickle", "rb") as file:
			words, labels, training, output = pickle.load(file)
		print("Loaded pickle")
		
		#yaml chatbotmodel.yaml
		download_blob(bucket, 'chatbotmodel.yaml', '/tmp/chatbotmodel.yaml')
		yaml_file = open('/tmp/chatbotmodel.yaml', 'r')
		loaded_model_yaml = yaml_file.read()
		yaml_file.close()
		print("Loaded yaml")
		
		#weight chatbotmodel.h5
		download_blob(bucket, 'chatbotmodel.h5', '/tmp/chatbotmodel.h5')
		model = model_from_yaml(loaded_model_yaml)
		model.load_weights("/tmp/chatbotmodel.h5")
		print("Loaded model")
		
		#punkt
		nltk.download('punkt')
		print("Loaded punkt")
		
	content = request.get_json()
	return chatWithBot(content["chat"])
    
	return class_names[numpy.argmax(predictions)]