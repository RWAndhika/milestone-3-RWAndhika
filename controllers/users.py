from flask import Blueprint, request
from connectors.mysql_connector import connection
from models.users import Users

from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from flask_login import login_user, logout_user, login_required, current_user

users_routes = Blueprint('users_routes', __name__)

Session = sessionmaker(connection)
s = Session()
# s.begin()

@users_routes.route('/users', methods=['POST'])
def register_user():
    # Session = sessionmaker(connection)
    # s = Session()

    # s.begin()
    try:
        NewUser = Users(username = request.form['username'], email = request.form['email'])
        NewUser.set_password(request.form['password_hash'])

        s.add(NewUser)
        s.commit()
    except Exception as e:
        print(e)
        s.rollback()
        return {'message': 'Fail to register'}, 500
    
    return {'message': 'Register user success'}, 200
    
@users_routes.route('/users/login', methods=['POST'])
def user_login():
    # Session = sessionmaker(connection)
    # s = Session()

    # s.begin()
    try:
        email = request.form['email']
        user = s.query(Users).filter(Users.email == email).first()

        if user == None:
            return {'message': 'User not found'}, 403

        if not user.check_password(request.form['password_hash']):
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
# @login_required
def info_user():
    try:
        return {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email
        }, 200
    except Exception as e:
        print(e)
        return {'message': 'Unauthorized'}, 401

@users_routes.route('/users/me', methods=['PUT'])
@login_required
def update_user():

    flag = False

    # Session = sessionmaker(connection)
    # s = Session()

    # s.begin()
    try:
        user = s.query(Users).filter(Users.id == current_user.id).first()

        if 'username' in request.form:
            user.username = request.form['username']
            flag = True
        if 'email' in request.form:        
            user.email = request.form['email']
            flag = True
        if flag:
            user.updated_at = func.now()
            # s.add(user)
            s.commit()
    
    except Exception as e:
        s.rollback()
        return {'message': 'Fail to update user'}, 500
    
    return {'message': 'Update user info success'}, 200

@users_routes.route('/users/me', methods=['DELETE'])
@login_required
def delete_user():
    # Session = sessionmaker(connection)
    # s = Session()
    
    # s.begin()
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
@login_required
def user_logout():
    logout_user()
    return {'message': 'Logout user success'}, 200
        