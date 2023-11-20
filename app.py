from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
import logging
import os
app = Flask(__name__)
log_handler = logging.FileHandler('flask_app.log')
log_handler.setLevel(logging.ERROR)
app.logger.addHandler(log_handler)
MONGODB_THRESHOLD=0
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('MYSQL_DATABASE_URI') or 'mysql://root:@localhost/log_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

mongo_uri = os.environ.get('MONGO_DATABASE_URI') or None
mongo_client = MongoClient(mongo_uri)

# Use the specified database and collection
mongo_db = mongo_client['log_database']
mongo_logs_collection = mongo_db['logs']

from views import *

with app.app_context():
    db.create_all()

