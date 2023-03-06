from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"] = "64be0cc808f5ff47f9754b3a1d80eeef62314fa0"
app.config["MONGO_URI"] = "mongodb+srv://gshantheep:cinadoc@cluster0.cz7xwta.mongodb.net/?retryWrites=true&w=majority"


mongodb_client = PyMongo(app)
db = mongodb_client.db
from application import routes