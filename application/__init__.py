from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"] = "6273599d09fa2a572dccfb8d79d801d7c1fdeb9d"
app.config["MONGO_URI"] = "mongodb+srv://sahuabhit27:8z2SEJDEnKYqWOUs@cluster0.pexos.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# mongodb database
mongodb_client = PyMongo(app)
db = mongodb_client.db

from application import routes
