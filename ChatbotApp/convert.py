import tensorflow as tf
from tensorflow.keras import models
from main import chatbotModel
import pathlib

export_dir = 'saved_model/l'
tf.saved_model.save(chatbotModel, export_dir)

converter = tf.lite.TFLiteConverter.from_saved_model(export_dir)
tflite_model = converter.convert()

file = pathlib.Path('chatbotmodel.tflite')
file.write_bytes(tflite_model)
