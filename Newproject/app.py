
from re import A
from flask import Flask, render_template, request ,redirect,url_for
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import os 

app = Flask(__name__)

model = tf.keras.models.load_model(r'D:\Basic Flask\Newproject\pork_classification_model')

def test_model(filename ,img_shape=224):
    """
    Reads in an image from filename, turns it into a tensor and reshapes into
    (224, 224, 3).
    """
    # Read in the image
    img = tf.io.read_file(filename)
    # Decode it into a tensor
    img = tf.image.decode_jpeg(img)
    # Resize the image
    img = tf.image.resize(img, [img_shape, img_shape])
    # Rescale the image (get all values between 0 and 1)
    img = img/255.

    #** Change size & dimention image
    img = tf.expand_dims(img, axis=0)
    resultOfModel = model.predict(img)
    result = resultOfModel.argmax()
    # model = [0.899531531 , 0.1232141241 , 0.321312]
    dict = {"percent":resultOfModel[0][result]*100,"beta_pork":resultOfModel[0][0]*100 ,"normal_pork":resultOfModel[0][2]*100,"parasite_pork":resultOfModel[0][1]*100}
    
    # a = 3.14
    # b = 2.03
    # c = 1.11
    a = 0
    b = 0
    c = 0
    dict['percent'] = dict['percent']-a
    if result == 0:
        final = "BetaAgonist Pork"
        dict['beta_pork'] = round(dict['beta_pork']-a,2)
        dict['normal_pork'] = round(dict['normal_pork']+b,2)
        dict['parasite_pork'] = round(dict['parasite_pork']+c,2)
    elif result == 1:
        final = "Parasite Pork"
        dict['beta_pork'] = round(dict['beta_pork']+c,2)
        dict['normal_pork'] = round(dict['normal_pork']+b,2)
        dict['parasite_pork'] = round(dict['parasite_pork']-a,2)
    elif result == 2:
        final = "Normal Pork"
        dict['beta_pork'] = round(dict['beta_pork']+c,2)
        dict['normal_pork'] = round(dict['normal_pork']-a,2)
        dict['parasite_pork'] = round(dict['parasite_pork']+b,2)
    dict['name'] = final

    

    return dict

@app.route('/',methods = ["GET"])
def index():
    return render_template("index.html")

@app.route('/',methods =["POST"])
def predict():

    imagefile = request.files['imagefile']
    image_path = r"D:\Basic Flask\Newproject\static\images2\Test" + imagefile.filename
    imagefile.save(image_path)
    n = "../static/images2/Test" + imagefile.filename
    picture = test_model(image_path) 
    name = picture['name'] + " "+str("{:.2f}".format(picture['percent']))

    return render_template("page2.html",prediction = name,normal_pork=picture['normal_pork'],parasite_pork=picture['parasite_pork'],
            beta_pork=picture['beta_pork'],picture = picture,n=n)
if __name__ == "__main__":
    app.run(debug=True)