from flask import Flask, jsonify,request, redirect, url_for, render_template
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

import numpy as np 
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

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

    #   Getting output from the model
model = load_model('acc71.h5')
model._make_predict_function()

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(255,255))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    return preds

if __name__ == "__main__":
    app.run(debug=True)






"""
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb+srv://gshantheep:cinadoc@cluster0.cz7xwta.mongodb.net/?retryWrites=true&w=majority')
db = client['Cinadoc']
collection = db['users']

@app.route('/')
def home():
    return "Hello"

@app.route('/add')
def insert_document():
    new_document = {
        'name': 'John Doe',
        'email': 'johndoe@example.com'
    }
    result = collection.insert_one(new_document)
    return f'Inserted document with ID: {result.inserted_id}'

if __name__ == '__main__':
    app.run(debug=True)
    """

"""
from flask import Flask, jsonify,request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash,check_password_hash
from pymongo import MongoClient
app = Flask(__name__) 

app.secret_key = "cinadoc"
app.config['MONGO_URI'] = "mongodb+srv://gshantheep:cinadoc@cluster0.cz7xwta.mongodb.net/?retryWrites=true&w=majority"

#client = MongoClient('mongodb+srv://gshantheep:cinadoc@cluster0.cz7xwta.mongodb.net/?retryWrites=true&w=majority')
#db = client['Cinadoc']
#collection = db['users']

mongo = PyMongo(app)


@app.route('/add',methods=['POST'])

def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _email and _password and request.method == 'POST':
        _hashed_password = generate_password_hash(_password)

        id = mongo.db.collection.insert({'name':_name, 'email':_email, 'pwd':_hashed_password})

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
app.run(port=27017)
if __name__ == "__main__":
    app.run(debug=True)
"""