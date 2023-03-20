from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re

from flask import Flask, jsonify,request, redirect, url_for, render_template
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import numpy as np 
from keras.applications import VGG19
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
import keras.utils as image
#from keras.preprocessing import image

app = Flask(__name__) 
app.secret_key = "cinadoc"
app.config['MONGO_URI'] = "mongodb://localhost:27017/Users"

mongo = PyMongo(app)


@app.route('/add',methods=['POST'])

def add_user():   
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _phone = _json['phone']
    _password = _json['pwd']

    if _name and _email and _password and _phone and request.method == 'POST':
        _hashed_password = generate_password_hash(_password)   
        id = mongo.db.user.insert_one({'name':_name, 'email':_email, 'phone':_phone, 'pwd':_hashed_password})
        resp = jsonify("User created")
        resp.status_code = 200
        return resp

    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message':'Not found' + request.url
    }
    resp = jsonify(message)

    resp.status_code = 404
    return resp

@app.route('/users')
def users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp

@app.route('/user/<id>')
def user(id):
    user = mongo.db.user.find_one({'_id':ObjectId(id)})
    resp = dumps(user)
    return resp

@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({'_id':ObjectId(id)})
    resp = jsonify("User deleted")
    resp.status_code = 200
    return resp

@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _phone = _json['phone']
    _password = _json['pwd']

    if _name and _email and _password and _phone and request.method == 'PUT':
        _hashed_password = generate_password_hash(_password)
    
        mongo.db.user.update_one({'_id': ObjectId(['$olid']) if '$olid' in _id else ObjectId(_id) }, {'$set': {'name':_name, 'email': _email,'pwd': _hashed_password}})
        resp = jsonify('User updated')
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/login')
def login():
    _json = request.json
    username = _json['name']
    password = _json['pwd']
    user = mongo.db.user.find_one({'name':username})
    if password == user['pwd']:
        return "Login success"
    else:
        return "Incorrect password"



model = load_model('acc73.h5')
model.make_predict_function()

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(255,255))
    x = image.img_to_array(img)
    x = np.expand_dims(img, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    return preds

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict',methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
    
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

       
        preds = model_predict(file_path, model)

        predicted_label = np.argmax(preds)

        if predicted_label == 0:
            result = "Rough Bark"
            return result
        else:
            result = "Stripe canker"
            return result
                    

if __name__ == "__main__":
    app.run(debug=True)






