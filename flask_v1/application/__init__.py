from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"] = "64be0cc808f5ff47f9754b3a1d80eeef62314fa0"
app.config["MONGO_URI"] = "mongodb://gshantheep:utmsaCdPlaOwcZdU@ac-bj5d9jb-shard-00-00.cz7xwta.mongodb.net:27017,ac-bj5d9jb-shard-00-01.cz7xwta.mongodb.net:27017,ac-bj5d9jb-shard-00-02.cz7xwta.mongodb.net:27017/?ssl=true&replicaSet=atlas-feqw05-shard-0&authSource=admin&retryWrites=true&w=majority"


mongodb_client = PyMongo(app)
db = mongodb_client.db
from application import routes