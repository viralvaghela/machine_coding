import datetime
import jwt

login_attempts = {}

def is_blocked(ip):
    attempts = login_attempts.get(ip, [])
    cutoff = datetime.datetime.now() - datetime.timedelta(minutes=15)
    login_attempts[ip] = [t for t in attempts if t > cutoff]
    return len(login_attempts[ip]) >= 5

def generate_token(user_id, secret_key):
    return jwt.encode({
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, secret_key, algorithm="HS256")
