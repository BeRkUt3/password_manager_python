from cryptography.fernet import Fernet
from database import check_root_data
import os
import sqlite3

if not os.path.exists('user_data.db'):
    with open('user_data.db', 'w') as f:
        pass
conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (   id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT,
    password TEXT
)
""")
conn.commit()

if not os.path.exists('crypt.key'):
    with open('crypt.key', 'wb') as f:
        f.write(Fernet.generate_key())

check_root_data()