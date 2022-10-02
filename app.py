import os
from flask import Flask, redirect, url_for, request, render_template, Response, redirect, send_from_directory
import numpy as np
from gevent.pywsgi import WSGIServer
from tensorflow.keras.preprocessing.image import load_img , img_to_array
import pickle

app = Flask(__name__, static_url_path='/static/image', static_folder = "static/image")

img_width, img_height = 180, 180

MODEL_PATH = 'models/modelmlh.pkl'

class_names = ['Pneumonia', 'Normal']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
# model = load_model(os.path.join(BASE_DIR , 'model.hdf5'))

with open(MODEL_PATH, 'rb') as file:  
    model = pickle.load(file)

def predict(filename , model):
    img = load_img(filename , target_size = (150 ,150))
    # img = img_to_array(img)
    frame = np.asarray(img)
    # frame = frame.astype('float32')
    # frame /= 255.0
    frame=np.expand_dims(frame, axis=0)
    # img = img.reshape(None, 180, 180 ,3)
    # img = img.astype('float32')
    # img = img/255.0
    result = model.predict(frame)
    # print(result)
    # dict_result = {}
    # for i in range(8):
    #     dict_result[result[0][i]] = class_names[i]
    # res = result[0]
    # res.sort()
    # res = res[::-1]
    # prob = res[:3]
    
    # prob_result = []
    # class_result = []
    # for i in range(3):
    #     prob_result.append((prob[i]*100).round(2))
    #     class_result.append(dict_result[prob[i]])

    output= str() 

    if result == 0:
        output = "Pneumonia"
    elif result == 1:
        output = "Normal"

    predd =" 90%"

    return output , predd 


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/', methods=[ 'POST'])
def predicter():
    target_img = os.path.join(os.getcwd() , 'static/images')
    file = request.files['imagefile']

    file.save(os.path.join(target_img , file.filename))
    img_path = os.path.join(target_img , file.filename)
    print(file.filename)
    class_result , prob_result = predict(img_path , model)
    result_text = "% s " % (class_result)
    return render_template('result.html', result_text=result_text, img_path="https://raw.githubusercontent.com/yuvaramd/pneumonia-pics/main/pics/"+file.filename)

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8999), app)
    http_server.serve_forever()