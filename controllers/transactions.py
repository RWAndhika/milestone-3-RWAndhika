from flask import Blueprint, request
from models.transactions import Transactions
from models.accounts import Accounts
from controllers.users import s

from sqlalchemy import func, or_, and_

from flask_login import login_required, current_user

transactions_routes = Blueprint('transactions_routes', __name__)


@transactions_routes.route('/transactions', methods=['GET'])
@login_required
def get_transactions():
    try:
        accounts = s.query(Accounts).filter(Accounts.user_id == current_user.id).all()
        account_ids = [account.id for account in accounts]

        if not account_ids:
            return {'transactions': []}, 200
        
        transactions_query = s.query(Transactions).filter(
            or_(
                Transactions.from_account_id.in_(account_ids),
                Transactions.to_account_id.in_(account_ids)
            )
        )
        result = s.execute(transactions_query)
        transactions = []

        for row in result.scalars():
            transactions.append(
                {
                    'id': row.id,
                    'from_account_id': row.from_account_id,
                    'to_account_id': row.to_account_id,
                    'amount': row.amount,
                    'type': row.type,
                    'description': row.description,
                    'created_at': row.created_at
                }
            )

        return {'transactions': transactions}, 200

    except Exception as e:
        return {'message': 'Unexpected error'}, 500
    
@transactions_routes.route('/transactions/<id>', methods=['GET'])
@login_required
def get_transaction(id):
    try:
        accounts = s.query(Accounts).filter(Accounts.user_id == current_user.id).all()
        account_ids = [account.id for account in accounts]
        print(account_ids)
        transaction = s.query(Transactions).filter(
            and_(
                Transactions.id == id,
                or_(
                    Transactions.from_account_id.in_(account_ids),
                    Transactions.to_account_id.in_(account_ids)
                )
            )
        ).first()
        
        if transaction == None:
            return {'message': 'Transaction not found'}, 403

        return {
            'id': transaction.id,
            'from_account_id': transaction.from_account_id,
            'to_account_id': transaction.to_account_id,
            'amount': transaction.amount,
            'type': transaction.type,
            'description': transaction.description,
            'created_at': transaction.created_at
            }, 200

    except Exception as e:
        return {'message': 'Unexpected error'}, 500

@transactions_routes.route('/transactions', methods=['POST'])
@login_required
def add_transaction():
    try:
        allowed_type = ['deposit', 'withdrawal', 'transfer']
        transaction_type = request.form['type']
        if transaction_type not in allowed_type:
            return {'message': 'Invalid transaction type (deposit, withdrawal, transfer)'}, 400
        
        user_accounts = s.query(Accounts).filter(Accounts.user_id == current_user.id).all()
        user_account_ids = [account.id for account in user_accounts]
        all_accounts = s.query(Accounts).all()
        all_account_ids = [account.id for account in all_accounts]

        NewTransaction = Transactions(
            type=transaction_type,
            amount=request.form['amount'],
            description=request.form['description']
        )

        if NewTransaction.type == 'deposit':
            to_account_id = request.form.get('to_account_id', type=int)
            if to_account_id and to_account_id in user_account_ids:
                NewTransaction.to_account_id = to_account_id
                account = s.query(Accounts).filter(Accounts.id == to_account_id).first()
                account.balance += int(NewTransaction.amount)
                account.updated_at = func.now()
            else:
                return {'message': 'Invalid to_account_id for deposit'}, 400

        elif NewTransaction.type == 'transfer':
            from_account_id = request.form.get('from_account_id', type=int)
            if from_account_id and from_account_id in all_account_ids:
                NewTransaction.from_account_id = from_account_id
                from_account = s.query(Accounts).filter(Accounts.id == from_account_id).first()
                if from_account.balance - int(NewTransaction.amount) >= 0:
                    from_account.balance -= int(NewTransaction.amount)
                    from_account.updated_at = func.now()
                else:
                    return {'message': 'Insufficient funds'}, 400
            else:
                return {'message': 'Invalid from_account_id for transfer'}, 400

            to_account_id = request.form.get('to_account_id', type=int)
            if to_account_id and to_account_id != from_account_id and to_account_id in all_account_ids:
                NewTransaction.to_account_id = to_account_id
                to_account = s.query(Accounts).filter(Accounts.id == to_account_id).first()
                to_account.balance += int(NewTransaction.amount)
                to_account.updated_at = func.now()
            else:
                return {'message': 'Invalid to_account_id for transfer'}, 400

        elif NewTransaction.type == 'withdrawal':
            from_account_id = request.form.get('from_account_id', type=int)
            if from_account_id and from_account_id in user_account_ids:
                NewTransaction.from_account_id = from_account_id
                account = s.query(Accounts).filter(Accounts.id == from_account_id).first()
                if account.balance - int(NewTransaction.amount) >= 0:
                    account.balance -= int(NewTransaction.amount)
                    account.updated_at = func.now()
                else:
                    return {'message': 'Insufficient funds'}, 400
            else:
                return {'message': 'Invalid from_account_id for withdrawal'}, 400

        s.add(NewTransaction)
        s.commit()
    
    except Exception as e:
        s.rollback()
        return {'message': 'Unexpected error'}, 500
    
    return {'message': 'Add transaction success'}, 200
