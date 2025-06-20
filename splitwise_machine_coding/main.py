from flask import Flask
from auth.routes import auth_bp
from db import init_db
from expenses.routes import expenses_bp

app = Flask(__name__)
app.config.from_pyfile('config.py')

init_db()
app.register_blueprint(auth_bp)
app.register_blueprint(expenses_bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
