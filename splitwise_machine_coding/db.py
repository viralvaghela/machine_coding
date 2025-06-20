import sqlite3
from config import DATABASE

conn = sqlite3.connect(DATABASE, check_same_thread=False)

def init_db():
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        mobile_number TEXT NOT NULL UNIQUE
    )'''
                   )

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paid_by INTEGER NOT NULL,
    amount REAL NOT NULL,
    split_type TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(paid_by) REFERENCES users(id)
                   ''')
    
    
    cursor.execute(
        '''

    

CREATE TABLE IF NOT EXISTS expense_shares (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_id INTEGER NOT NULL,
    owed_by INTEGER NOT NULL,
    owed_to INTEGER NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY(expense_id) REFERENCES expenses(id),
    FOREIGN KEY(owed_by) REFERENCES users(id),
    FOREIGN KEY(owed_to) REFERENCES users(id)
)
'''
    )


    
    conn.commit()
    cursor.close()

def get_db():
    return conn
