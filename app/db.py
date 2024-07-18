from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import current_app, g
from werkzeug.local import LocalProxy
from dotenv import load_dotenv
import os


load_dotenv()


def get_db():
    if 'db' not in g:
        try:
            uri = os.getenv('MONGO_URI')
            client = MongoClient(uri, server_api=ServerApi('1'))
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            g.db_client = client
            g.db = client['Monitor']
        except Exception as e:
            raise Exception(f"The following error occurred: {e}")
    return g.db

def close_db(e=None):

    db_client = g.pop('db_client', None)
    if db_client is not None:
        db_client.close()
        print("Database connection closed")


db = LocalProxy(get_db)

def init_app(app):

    app.teardown_appcontext(close_db)
