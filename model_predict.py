import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

classification = ["covid", "normal"]
def prepare(filepath):
    IMG_SIZE = 500
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

def predict_covid(imagepath):
    model = tf.keras.models.load_model("covid19cnn.model")
    image = cv2.imread(imagepath, cv2.IMREAD_COLOR)
    image = cv2.resize(image, (1500,1500))
    img_array = cv2.imread(imagepath, cv2.IMREAD_COLOR)
    img_array = cv2.resize(img_array, (1500,1500))
    prediction = model.predict([prepare(imagepath)])
    label = str(classification[int(prediction[0][0])])
    if label == 'covid':
        return("positive")
    else:
        return "negative"

cv2.destroyAllWindows()


