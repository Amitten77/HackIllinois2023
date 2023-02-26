import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import cv2
import urllib
import itertools
import random, os, glob
from imutils import paths
from sklearn.utils import shuffle
from urllib.request import urlopen
import warnings
warnings.filterwarnings("ignore")
from sklearn.metrics import confusion_matrix, classification_report
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import  ModelCheckpoint, EarlyStopping
from tensorflow.keras.layers import Conv2D, Flatten, MaxPooling2D, Dense, Dropout, SpatialDropout2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img, array_to_img
import os
from keras.models import load_model
from PIL import Image
import csv
import fileinput
from autocorrect import Speller
import webcolors
from math import sqrt
from flask import Flask


app = Flask(__name__)


def CNN_model_testing(path, model, dic):
  img = image.load_img(path, target_size=(224,224,3))
  img = image.img_to_array(img, dtype=np.uint8)
  img = np.array(img)/255.0
  p = model.predict(img.reshape(1,224,224,3))
  predicted_class = np.argmax(p[0])
  return img, dic[predicted_class], p[0][predicted_class]

def get_average(filepath, oripath):
    im = Image.open(filepath) # Can be many different formats.
    pix = im.load()
    pixel_dic = {}
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            rgba = pix[i, j]
            if rgba in pixel_dic:
                pixel_dic[rgba].append((i, j))
            else:
                pixel_dic[rgba] = [(i, j)]
    maximum = -1
    best_key = ""
    for key in pixel_dic:
        if (maximum == -1):
            maximum = len(pixel_dic[key])
            best_key = key
        else:
            if len(pixel_dic[key]) < maximum:
                best_key = key
    average = [0, 0, 0]
    im_glass = Image.open(oripath) # Can be many different formats.
    pix_glass = im_glass.load()
    for pixel in pixel_dic[best_key]:
        a, b, c = pix_glass[pixel[0], pixel[1]]
        average[0] += a
        average[1] += b
        average[2] += c
    average[0] = float(average[0] / len(pixel_dic[best_key]))
    average[1] = float(average[1] / len(pixel_dic[best_key]))
    average[2] = float(average[2] / len(pixel_dic[best_key]))
    return average

# SEGMENTATION
def image_segment(filepath, outpath):
    img = cv2.imread(filepath)
    b,g,r = cv2.split(img)
    rgb_img = cv2.merge([r,g,b])
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # noise removal
    kernel = np.ones((2,2),np.uint8)
    #opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
    closing = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel, iterations = 2)
    # sure background area
    sure_bg = cv2.dilate(closing,kernel,iterations=3)
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(sure_bg,cv2.DIST_L2,3)
    # Threshold
    ret, sure_fg = cv2.threshold(dist_transform,0.1*dist_transform.max(),255,0)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)
    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1
    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0
    markers = cv2.watershed(img,markers)
    img[markers == -1] = [255,0,0]
    #plt.subplot(211),plt.imshow(rgb_img)
    plt.imsave(outpath,thresh)
    return get_average(outpath, filepath)
    
def determine_color(r, g, b):
    white = [145, 138, 126]
    brown = [73, 56, 50]
    green = [75, 108, 73]
    white_dis = pow(white[0] - r, 2) + pow(white[1] - g, 2) + pow(white[2] - b, 2)
    brown_dis = pow(brown[0] - r, 2) + pow(brown[1] - g, 2) + pow(brown[2] - b, 2)
    green_dis = pow(green[0] - r, 2) + pow(green[1] - g, 2) + pow(green[2] - b, 2)
    if (min(white_dis, brown_dis, green_dis) == white_dis):
        return "white"
    if (min(white_dis, brown_dis, green_dis) == green_dis):
        return "green"
    return "brown"

def find_color(filepath, outpath):
    value = image_segment(filepath, outpath)
    return determine_color(value[0], value[1], value[2])


def what_is_this(filepath):
    trash_dic = {0: "cardboard", 1: "glass", 2: "metal", 3: "paper", 4: "plastic", 5: "trash"}
    electronic_dic = {0: "keyboard", 1: "mouse", 2: "computer"}
    fruit_dic = {0: "apple", 1: "banana", 2: "beetroot", 3: "bell pepper", 4: "cabbage", 5: "capsicum", 6: "carrot", 7: "cauliflower", 8: "chilli pepper", 9: "corn", 10: "cucumber", 11: "eggplant", 12: "garlic", 13: "ginger", 14: "grapes", 15: "jalepeno", 16: "kiwi", 17: "lemon", 18: "lettuce", 19: "mango", 20: "onion", 21: "orange", 22: "paprika", 23: "pear", 24: "peas", 25: "pineapple", 26: "pomegranate", 27: "potato", 28: "raddish", 29: "soy beans", 30: "spinach", 31: "sweetcorn", 32: "sweet potato", 33: "tomato", 34: "turnip", 35: "watermelon"}
    #trash_model = load_model('./Models/genericmodel.h5') #uncomment if models need to be reloaded
    #fruit_model = load_model('./Models/fruitmodel.h5')
    #electronic_model = load_model('./Models/electronicmodel.h5')
    img, trash_class, trash_cert = CNN_model_testing(filepath, trash_model, trash_dic)
    print(trash_class, trash_cert)
    img, fruit_class, fruit_cert = CNN_model_testing(filepath, fruit_model, fruit_dic)
    print(fruit_class, fruit_cert)
    img, electronic_class, electronic_cert = CNN_model_testing(filepath, electronic_model, electronic_dic)
    print(electronic_class, electronic_cert)
    if fruit_cert > .9:
        return fruit_class
    if trash_cert > .9:
        if trash_class == "glass":
            color = find_color(filepath, "./glassout/output.png")
            return color + " " + trash_class
        return trash_class
    if electronic_cert > .8:
        return electronic_class
    else:
        return "Not Found"

# finds closest of brown, green, white for parameter color
def closest_color(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in COLORS:
        cr, cg, cb = color
        color_diff = sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]

# returns closest of brown, green, white glass
def ans_color(rgb):
    if (rgb == (128, 96, 77)):
        return "brown"
    if (rgb ==  (0, 255, 0)):
        return "green"
    if (rgb == (255, 255, 255)):
        return "white"    
    
    
@app.route('/<val>')  
def place_in_bucket(val):
    val = val.lower()
    if val == "green glass":
        return val
    if val == "white glass":
        return val
    if val == "brown glass":
        return val
    # bool to check if spellcheck functionality is needed
    found = False
    # create spell check
    spell = Speller()

    # empty array to store all matching bins
    bins = []
    bin = "yes"

    # int rgb codes for brown, green, white for classifying glass
    COLORS = (
        (128, 96, 77),
        (0, 255, 0),
        (255, 255, 255)
    )
    with open('./csvs/final_trash.csv') as file_obj:
        # Create reader object by passing the file 
        reader_obj = csv.reader(file_obj)
        # looks through trash.csv and spellchecks input
        for row in reader_obj:
            for element in row[1:]:
                if (val in element):
                  found = True
        if found is False:
           val = spell(val)
        file_obj.close()

    # opening final_trash.csv again to classify items
    with open('./csvs/final_trash.csv') as file_obj:   
        reader_obj = csv.reader(file_obj)
        # Iterate over each row in the csv file using reader object
        # iterate over each element in row and check if value is in element, and if in element, append proper bin color
        for row in reader_obj:
            for element in row[1:]:
                if (val == element):
                    return row[0]
                elif (val in element):
                        bins.append(row[0])
    # sorts input into proper bin using our system of priority
    # if input is not found, goes to black
    if (len(bins) == 0):
        return "black"
    # if input fits in bin and is contaminated with brown (organic material), goes to black
    else:
        if ('brown' in bins and ('red' in bins or 'glass' in bins or 'yellow' in bins or 'blue' in bins or 'black' in bins)):
            bin = "black"
        elif ('red' in bins):
            bin = "red"
        elif ('glass' in bins):
            bin = "glass"
        elif ('yellow' in bins):
            bin = "yellow"
        elif ('brown' in bins):
            bin = "brown"
        elif ('blue' in bins):
            bin = "blue"
        elif ('black' in bins):
            bin = "black"
    # sorts glass into proper colored glass bin
    if (bin == "glass"):
        return "white glass"
    else:
        return bin

@app.route('/image')
def image_to_bucket(filepath):
    obj = what_is_this(filepath)
    if obj == "Not Found":
        return "Prompt User"
    else:
        return place_in_bucket(obj)
    
trash_model = load_model('./Models/genericmodel.h5')
fruit_model = load_model('./Models/fruitmodel.h5')
electronic_model = load_model('./Models/electronicmodel.h5')

trash_dic = {0: "cardboard", 1: "glass", 2: "metal", 3: "paper", 4: "plastic", 5: "trash"}
electronic_dic = {0: "keyboard", 1: "mouse", 2: "computer"}
fruit_dic = {0: "apple", 1: "banana", 2: "beetroot", 3: "bell pepper", 4: "cabbage", 5: "capsicum", 6: "carrot", 7: "cauliflower", 8: "chilli pepper", 9: "corn", 10: "cucumber", 11: "eggplant", 12: "garlic", 13: "ginger", 14: "grapes", 15: "jalepeno", 16: "kiwi", 17: "lemon", 18: "lettuce", 19: "mango", 20: "onion", 21: "orange", 22: "paprika", 23: "pear", 24: "peas", 25: "pineapple", 26: "pomegranate", 27: "potato", 28: "raddish", 29: "soy beans", 30: "spinach", 31: "sweetcorn", 32: "sweet potato", 33: "tomato", 34: "turnip", 35: "watermelon"}

print(image_to_bucket("./TestImages/lemon.png"))

if __name__ == '__main__':
    app.run(debug=True)