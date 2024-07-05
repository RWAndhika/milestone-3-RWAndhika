from flask import Blueprint, request
from connectors.mysql_connector import connection
from models.users import Users

from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from flask_login import login_user, logout_user, current_user
from decorators.authorization_checker import auth_required

from cerberus import Validator
from validations.users_validation import users_register_schema, users_update_schema

users_routes = Blueprint('users_routes', __name__)

Session = sessionmaker(connection)
s = Session()

@users_routes.route('/users', methods=['POST'])
def register_user():

    v = Validator(users_register_schema)
    request_body = {
        'username': request.form.get('username'),
        'email': request.form.get('email')
    }

    if not v.validate(request_body):
        return {'error': v.errors}, 409

    try:
        NewUser = Users(username=request.form['username'], email=request.form['email'])
        NewUser.set_password(request.form['password'])

        s.add(NewUser)
        s.commit()
    except Exception as e:
        s.rollback()
        return {'message': 'Fail to register'}, 500
    
    return {'message': 'Register user success'}, 200
    
@users_routes.route('/users/login', methods=['POST'])
def user_login():
    try:
        email = request.form['email']
        user = s.query(Users).filter(Users.email == email).first()

        if user == None:
            return {'message': 'User not found'}, 403

        if not user.check_password(request.form['password']):
            return {'message': 'Invalid password'}, 403
        
        login_user(user)
        session_id = request.cookies.get('session')
        return {
            'session_id': session_id,
            'message': 'Login success'
        }, 200
    
    except Exception as e:
        s.rollback()
        return {'message': 'Fail to login'}, 500
    
@users_routes.route('/users/me', methods=['GET'])
@auth_required()
def info_user():
    try:
        return {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'created_at': current_user.created_at,
            'updated_at': current_user.updated_at
        }, 200
    except Exception as e:
        return {'message': 'Unauthorized'}, 401

@users_routes.route('/users/me', methods=['PUT'])
@auth_required()
def update_user():

    v = Validator(users_update_schema)
    flag = False
    current_username = current_user.username
    current_email = current_user.email

    try:
        user = s.query(Users).filter(Users.id == current_user.id).first()

        if 'username' in request.form:
            request_body = {
                'username': request.form.get('username')
            }
            if not v.validate(request_body):
                s.rollback()
                return {'error': v.errors}, 409
            user.username = request.form['username']
            flag = True
        if 'email' in request.form:
            request_body = {
                'email': request.form.get('email')
            }
            if not v.validate(request_body):
                s.rollback()
                return {'error': v.errors}, 409        
            user.email = request.form['email']
            flag = True
        if flag:
            if 'password' in request.form:
                if user.username == current_username and user.email == current_email and user.check_password(request.form['password']):
                    s.rollback()
                    return {'message': 'No user info updated'}, 400
                user.set_password(request.form['password'])
            else:
                if user.username == current_username and user.email == current_email:
                    s.rollback()
                    return {'message': 'No user info updated'}, 400
                
            user.updated_at = func.now()
            s.commit()
        else:
            return {'message': 'No user info updated'}, 400
    
    except Exception as e:
        s.rollback()
        return {'message': 'Fail to update user'}, 500
    
    return {'message': 'Update user info success'}, 200

@users_routes.route('/users/me', methods=['DELETE'])
@auth_required()
def delete_user():
    try:
        user = s.query(Users).filter(Users.id == current_user.id).first()
        s.delete(user)
        s.commit()
        logout_user()
    except Exception as e:
        s.rollback()
        return {'message': 'Fail to delete user'}, 500
    
    return {'message': 'Delete user success'}, 200

@users_routes.route('/users/logout', methods=['GET'])
@auth_required()
def user_logout():
    logout_user()
    return {'message': 'Logout user success'}, 200
        