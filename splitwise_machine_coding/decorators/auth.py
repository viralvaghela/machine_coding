from flask import request, jsonify, current_app
from functools import wraps
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = data['user_id']
        except:
            return jsonify({'error': 'Token is invalid!'}), 401
        return f(user_id, *args, **kwargs)
    return decorated
