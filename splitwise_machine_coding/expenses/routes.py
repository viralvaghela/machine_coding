from flask import Blueprint, request, jsonify
from db import get_db
from flask import current_app
from decorators.auth import token_required
import datetime

expenses_bp = Blueprint('expenses', __name__, url_prefix='/api')

@expenses_bp.route('/expenses', methods=['POST'])
@token_required
def add_expense(payer_id):
    data = request.get_json()
    amount = float(data.get('amount'))
    participants = list(map(int, data.get('participants', [])))

    split_type = data.get('split_type')
    description = data.get('description', '')
    shares = data.get('shares', [])

    if not participants or payer_id not in participants:
        return jsonify({'error': 'Payer must be among participants'}), 400

    if split_type not in ['EQUAL', 'EXACT', 'PERCENT']:
        return jsonify({'error': 'Invalid split type'}), 400

    owed_list = []

    if split_type == 'EQUAL':
        base = round(amount / len(participants), 2)
        diff = round(amount - base * (len(participants) - 1), 2)
        for i, user in enumerate(participants):
            share = diff if i == 0 else base
            owed_list.append((user, share))

    elif split_type == 'EXACT':
        if not shares or round(sum(shares), 2) != round(amount, 2):
            return jsonify({'error': 'Shares do not add up to amount'}), 400
        owed_list = list(zip(participants, shares))

    elif split_type == 'PERCENT':
        if not shares or round(sum(shares), 2) != 100:
            return jsonify({'error': 'Percent must add to 100'}), 400
        owed_list = [(user, round(amount * pct / 100, 2)) for user, pct in zip(participants, shares)]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (paid_by, amount, split_type, description) VALUES (?, ?, ?, ?)',
                   (payer_id, amount, split_type, description))
    expense_id = cursor.lastrowid

    for user, share in owed_list:
        if user != payer_id:
            cursor.execute('INSERT INTO expense_shares (expense_id, owed_by, owed_to, amount) VALUES (?, ?, ?, ?)',
                           (expense_id, user, payer_id, share))

    conn.commit()
    cursor.close()

    return jsonify({'message': 'Expense added'}), 201


@expenses_bp.route('/balances', methods=['GET'])
def get_balances():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT owed_by, owed_to, ROUND(SUM(amount), 2)
        FROM expense_shares
        GROUP BY owed_by, owed_to
        HAVING SUM(amount) != 0
    ''')
    rows = cursor.fetchall()
    cursor.close()

    return jsonify({'balances': [{'from': row[0], 'to': row[1], 'amount': row[2]} for row in rows]})


@expenses_bp.route('/user/<user_id>/balance', methods=['GET'])
def get_user_balance(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT owed_by, owed_to, ROUND(SUM(amount), 2)
        FROM expense_shares
        WHERE owed_by = ? OR owed_to = ?
        GROUP BY owed_by, owed_to
        HAVING SUM(amount) != 0
    ''', (user_id, user_id))
    rows = cursor.fetchall()
    cursor.close()

    return jsonify({
        'user_id': user_id,
        'balances': [{'from': row[0], 'to': row[1], 'amount': row[2]} for row in rows]
    })
