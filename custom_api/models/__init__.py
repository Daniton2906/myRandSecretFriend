import mongoengine as db
import os

db_name = 'test'
db_host = 'localhost'
if 'MONGO_DB' in os.environ and 'MONGO_HOST' in os.environ:
    db_name = os.environ['MONGO_DB']
    db_host = os.environ['MONGO_HOST']
db.connect(db_name, host=db_host, port='', username='', password='')