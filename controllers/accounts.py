from flask import Blueprint, request
from models.accounts import Accounts
from controllers.users import s

from sqlalchemy import func

from flask_login import login_required, current_user

accounts_routes = Blueprint('accounts_routes', __name__)

@accounts_routes.route('/accounts', methods=['GET'])
@login_required
def get_accounts():
    try:
        accounts = s.query(Accounts).filter(Accounts.user_id == current_user.id)
        result = s.execute(accounts)
        accounts = []

        for row in result.scalars():
            accounts.append({
                'id': row.id,
                'user_id': row.user_id,
                'account_type': row.account_type,
                'account_number': row.account_number,
                'balance': row.balance,
                'created_at': row.created_at,
                'updated_at': row.updated_at
            })

        return {'accounts': accounts}, 200
    
    except Exception as e:
        return {'message': 'Unexcpected error'}, 500
    
@accounts_routes.route('/accounts/<id>', methods=['GET'])
@login_required
def get_account(id):
    try:
        account = s.query(Accounts).filter(Accounts.id == id).first()
        if not account.user_id == current_user.id:
            return {'message': 'Unauthorized'}
        if account == None:
            return {'message': "Account not found"}, 403

        return {
            'id': account.id,
            'user_id': account.user_id,
            'account_type': account.account_type,
            'account_number': account.account_number,
            'balance': account.balance,
            'created_at': account.created_at,
            'updated_at': account.updated_at
            }, 200
    
    except Exception as e:
        return {'message': 'Unexcpected error'}, 500
    
@accounts_routes.route('/accounts', methods=['POST'])
@login_required
def register_account():
    try:
        NewAccount = Accounts(
            user_id = current_user.id,
            account_type =  request.form['account_type'],
            account_number = request.form['account_number'],
            balance = request.form['balance']
        )

        s.add(NewAccount)
        s.commit()
    
    except Exception as e:
        s.rollback()
        return {'message': 'Unexcpected error'}, 500
    
    return {'message': 'Create a new account success'}, 200

@accounts_routes.route('/accounts/<id>', methods=['PUT'])
@login_required
def update_account(id):
    flag = False

    try:
        account = s.query(Accounts).filter(Accounts.id == id).first()
        if not account.user_id == current_user.id:
            return {'message': 'Unauthorized'}
        if 'account_type' in request.form:
            account.account_type = request.form['account_type']
            flag = True
        if 'account_number' in request.form:
            account.account_number = request.form['account_number']
            flag = True
        if 'balance' in request.form:        
            account.balance = request.form['balance']
            flag = True
        if flag:
            account.updated_at = func.now()
            s.commit()
    
    except Exception as e:
        s.rollback()
        return {'message': 'Fail to update account info'}, 500
    
    return {'message': 'Update account info success'}, 200

@accounts_routes.route('/accounts/<id>', methods=['DELETE'])
@login_required
def delete_account(id):
    try:
        account = s.query(Accounts).filter(Accounts.id == id).first()
        s.delete(account)
        s.commit()
    except Exception as e:
        s.rollback()
        return {'message': 'Fail to delete account'}, 500
    
    return {'message': 'Delete account success'}, 200
