from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from auth.utils import generate_token, is_blocked, login_attempts
from decorators.auth import token_required
from db import get_db
import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/registration', methods=['POST'])
def register_user():
    conn = get_db()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    mobile_number = data.get('mobile_number')

    if not all([username, password, email, mobile_number]):
        return jsonify({'error': 'Missing required fields'}), 400

    if len(username) < 3 or len(username) > 20:
        return jsonify({'error': 'Username must be between 3 and 20 characters'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400
    if '@' not in email or '.' not in email.split('@')[-1]:
        return jsonify({'error': 'Invalid email address'}), 400
    if len(mobile_number) != 10 or not mobile_number.isdigit():
        return jsonify({'error': 'Mobile number must be 10 digits'}), 400

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? OR email = ? OR mobile_number = ?',
                   (username, email, mobile_number))
    if cursor.fetchone():
        return jsonify({'error': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    cursor.execute('INSERT INTO users (username, password, email, mobile_number) VALUES (?, ?, ?, ?)',
                   (username, hashed_password, email, mobile_number))
    conn.commit()
    cursor.close()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login_user():
    conn = get_db()
    data = request.get_json()
    identifier = data.get('identifier') or data.get('username')
    password = data.get('password')
    ip = request.remote_addr

    if not identifier or not password:
        return jsonify({'error': 'Identifier and password required'}), 400

    if is_blocked(ip):
        return jsonify({'error': 'Too many failed login attempts'}), 429

    cursor = conn.cursor()
    cursor.execute('SELECT id, password FROM users WHERE username = ? OR email = ? OR mobile_number = ?',
                   (identifier, identifier, identifier))
    user = cursor.fetchone()
    cursor.close()

    if not user or not check_password_hash(user[1], password):
        login_attempts.setdefault(ip, []).append(datetime.datetime.now())
        return jsonify({'error': 'Invalid credentials'}), 401

    login_attempts[ip] = []  # reset attempts
    token = generate_token(user[0], current_app.config['SECRET_KEY'])
    return jsonify({'message': 'Login successful', 'token': token}), 200

@auth_bp.route('/profile', methods=['GET'])
@token_required
def profile(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT username, email, mobile_number FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'username': user[0], 'email': user[1], 'mobile_number': user[2]}), 200
