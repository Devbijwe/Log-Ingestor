from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
import logging
app = Flask(__name__)
log_handler = logging.FileHandler('flask_app.log')
log_handler.setLevel(logging.ERROR)
app.logger.addHandler(log_handler)
MONGODB_THRESHOLD=0
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/log_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

mongo_uri = "mongodb+srv://log_ingester_user:Log_1234@logingester.ybpxzug.mongodb.net/?retryWrites=true&w=majority"
mongo_client = MongoClient(mongo_uri)

# Use the specified database and collection
mongo_db = mongo_client['log_database']
mongo_logs_collection = mongo_db['logs']

from views import *

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=3000,host="0.0.0.0")