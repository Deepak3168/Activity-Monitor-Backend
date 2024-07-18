from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from .config import Config
from dotenv import load_dotenv
from flask_cors import CORS
import os


bcrypt = Bcrypt()
jwt = JWTManager()
mongo = PyMongo()
cors = CORS()
load_dotenv()



def create_app():
    app = Flask(__name__)
    with app.app_context():
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
        app.config['MONGO_URI'] = os.getenv('MONGO_URI')


        mongo.init_app(app,)
        print("Databse Connected")
        bcrypt.init_app(app)
        jwt.init_app(app)
        cors.init_app(app)
        
        from .auth import auth_blueprint
        from .logdata import logdata_blueprint
        app.register_blueprint(auth_blueprint)
        app.register_blueprint(logdata_blueprint)
    
    return app
