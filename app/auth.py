from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, unset_jwt_cookies, jwt_required, get_jwt_identity
from .models import User, LogData
from . import db, bcrypt
from datetime import datetime

auth_blueprint = Blueprint('auth', __name__)

class Authentication:

    @staticmethod
    @auth_blueprint.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data['username']
        password = data['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            user.last_login = datetime.utcnow()
            db.session.commit()

            # Log the login activity
            log = LogData(username=username, logtype='login')
            db.session.add(log)
            db.session.commit()

            return jsonify({'message': 'Login Success', 'access_token': access_token, 'refresh_token': refresh_token})
        else:
            return jsonify({'message': 'Login Failed'}), 401

    @staticmethod
    @auth_blueprint.route('/logout', methods=['POST'])
    @jwt_required()
    def logout():
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user:
            user.last_logout = datetime.utcnow()
            db.session.commit()

            # Log the logout activity
            log = LogData(username=user.username, logtype='logout')
            db.session.add(log)
            db.session.commit()

        response = jsonify({"msg": "Logout successful"})
        unset_jwt_cookies(response)
        return response

    @staticmethod
    @auth_blueprint.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data['username']
        password = data['password']
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'message': 'Username already exists'}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
    
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201
