from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt

from flask_jwt_extended import create_access_token, create_refresh_token, unset_jwt_cookies, jwt_required, get_jwt_identity
from datetime import datetime
from .db import db 
from bson.objectid import ObjectId 


bcrypt = Bcrypt()
auth_blueprint = Blueprint('auth', __name__)

class Authentication:
    @staticmethod
    @auth_blueprint.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data['username']
        password = data['password']
        
        existing_user = db.users.find_one({'username': username})
        if existing_user:
            return jsonify({'message': 'Username already exists'}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = {'username': username, 'password': hashed_password}
        db.users.insert_one(new_user)

        return jsonify({'message': 'User created successfully'}), 201

    @staticmethod
    @auth_blueprint.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Missing JSON in request'}), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Missing username or password'}), 400

        user = db.users.find_one({'username': username})
        if not user or not bcrypt.check_password_hash(user.get('password', ''), password):
            return jsonify({'message': 'Invalid username or password'}), 401

        access_token = create_access_token(identity=str(user['_id']))
        refresh_token = create_refresh_token(identity=str(user['_id']))


        db.users.update_one({'_id': user['_id']}, {'$set': {'last_login': datetime.utcnow()}})

        # Log the login action
        log = {'username': username, 'logtype': 'login', 'timestamp': datetime.utcnow()}
        db.log_data.insert_one(log)

        return jsonify({'message': 'Login Success', 'access_token': access_token, 'refresh_token': refresh_token}), 200

    @staticmethod
    @auth_blueprint.route('/logout', methods=['POST'])
    @jwt_required()
    def logout():
        current_user_id = get_jwt_identity()
        user = db.users.find_one({'_id': ObjectId(current_user_id)})
        if user:
       
            db.users.update_one({'_id': ObjectId(current_user_id)}, {'$set': {'last_logout': datetime.utcnow()}})

        
            log = {'username': user['username'], 'logtype': 'logout'}
            db.log_data.insert_one(log)

        response = jsonify({"msg": "Logout successful"})
        unset_jwt_cookies(response)
        return response

