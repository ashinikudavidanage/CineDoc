from flask import Flask, jsonify,request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__) 
app.secret_key = "cinadoc"
app.config['MONGO_URI'] = "mongodb://localhost:27017/Users"

mongo = PyMongo(app)


@app.route('/add',methods=['POST'])

def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _email and _password and request.method == 'POST':
        _hashed_password = generate_password_hash(_password)

        id = mongo.db.user.insert_one({'name':_name, 'email':_email, 'pwd':_hashed_password})

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