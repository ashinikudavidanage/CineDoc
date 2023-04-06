# Importing necessary libraries
import os
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import bcrypt
import numpy as np 
from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model
import keras.utils as image
from pymongo import MongoClient
from werkzeug.utils import secure_filename

# Setting up mongodb
app = Flask(__name__) 
app.secret_key = "cinadoc"
app.config['MONGO_URI'] = "mongodb+srv://gshantheep:cinadoc@cluster0.cz7xwta.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(app.config['MONGO_URI'])
db = client.get_database('Users')
collection = db.get_collection('user')
mongo = PyMongo(app)

# User registeration
@app.route('/register',methods=['POST'])
def register_user():   
    # Extracting values from dictionary
    data = request.json
    username = data['name']
    email = data['email']
    phone = data['phone']
    # Pswd encryption
    encrypted_pswd = bcrypt.hashpw(data['pwd'].encode('utf-8'), bcrypt.gensalt()) 
    # Existing username check
    existing_user = collection.find_one({'name': username})

    try:
        if username and email and encrypted_pswd and phone and request.method == 'POST':
            if existing_user:
                response = jsonify("Username already taken")
                response.status_code = 400
                return response
            
            else:
                id = collection.insert_one({'name':username, 'email':email, 'phone':phone, 'pwd':encrypted_pswd })
                response = jsonify("User created successfully!")
                response.status_code = 200
                return response                 
            
        else:
            response = jsonify("Required fields are empty")
            response.status_code = 400
            return response             
 
    except:
        response = jsonify("Something went wrong. Please try again")
        response.status_code = 400
        return response    

    
# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['name']
    password = data['pwd']

    if username and password :
        try:
            user = collection.find_one({'name':username})
            # decrypting password
            if bcrypt.checkpw(password.encode('utf-8'), user['pwd']):
                response = jsonify("Login success")
                response.status_code = 200
                return response 

            else:
                response = jsonify("Incorrect username or password")
                response.status_code = 400
                return response 
        except:
            response = jsonify("Incorrect username or password")
            response.status_code = 400
            return response 
    else:
        response = jsonify("Required fields are empty")
        response.status_code = 400
        return response 

# Prediction
model = load_model('acc73.h5')
model.make_predict_function()

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(255,255))
    x = image.img_to_array(img)
    x = np.expand_dims(img, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    return preds

@app.route('/predict',methods=['GET','POST'])
def upload():
    try:
        # Getting img from form data  & saving inside upload folder
        f = request.files['image']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # passing the img to model_predict()
        preds = model_predict(file_path, model)
        predicted_label = np.argmax(preds)

        if predicted_label == 0:
            response = jsonify("Rough Bark")
            response.status_code = 200
            return response 
        
        else:
            response = jsonify("Stripe canker")
            response.status_code = 200
            return response 
    except:
        response = jsonify("Image upload unsuccessful. Please try again")
        response.status_code = 400
        return response 
                    
if __name__ == "__main__":
    app.run(debug = True)






