from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .config import Config


db = SQLAlchemy()

bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
   
    from .auth import auth_blueprint
    from .logdata import logdata_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(logdata_blueprint)
    
    return app