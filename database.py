from argon2 import PasswordHasher
from cryptography.fernet import Fernet
import sqlite3

ph = PasswordHasher()

conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT,
    password TEXT
)
""")
conn.commit()

def check_root_data():
    cursor.execute(
        "SELECT password FROM passwords WHERE login = ?",
        ('root',)
    )
    row = cursor.fetchone()

    if row is None:
        cursor.execute(
            "INSERT INTO passwords (login, password) VALUES (?, ?)",
            ('root', ph.hash('0000'))
        )
        conn.commit()



def add_new_line(login, password):
    cursor.execute("""SELECT login FROM passwords WHERE login = ?""", (login,))
    row = cursor.fetchone()

    if row is None:

        cursor.execute("""INSERT INTO passwords (login, password) VALUES (?, ?)""", (login, encrypt_password(password)))
        conn.commit()
        return 'Login added successfully!'
    else:
        return "Password for this login already exists!"

def change_root_password(current_password, new_password):
    check_root_data()

    cursor.execute(
        "SELECT password FROM passwords WHERE login = ?",
        ('root',)
    )
    row = cursor.fetchone()

    stored_hash = row[0]

    try:
        ph.verify(stored_hash, current_password)
    except Exception:
        return 'Incorrect current password'

    new_hash = ph.hash(new_password)
    cursor.execute(
        "UPDATE passwords SET password = ? WHERE login = 'root'",
        (new_hash,)
    )
    conn.commit()

    return 'Password changed successfully!'

def check_root_password(current_password):
    cursor.execute(
        "SELECT password FROM passwords WHERE login = ?",
        ('root',)
    )
    row = cursor.fetchone()

    stored_hash = row[0]

    try:
        ph.verify(stored_hash, current_password)
        return True
    except Exception:
        return False

def decrypt_password(password):
    with open("crypt.key", "rb") as file:
        key = file.read()
    fernet = Fernet(key)
    return fernet.decrypt(password).decode()

def delete_line(id):
    cursor.execute("""DELETE FROM passwords WHERE id = ?""", (id,))
    conn.commit()


def edit_line_login(id, login):
    cursor.execute("""UPDATE passwords SET login = ? WHERE id = ?""", (login, id))
    conn.commit()

def edit_line_password(id, password):
    cursor.execute("""UPDATE passwords SET password = ? WHERE id = ?""", (encrypt_password(password), id))
    conn.commit()

def encrypt_password(password):
    with open("crypt.key", "rb") as file:
        key = file.read()
    fernet = Fernet(key)
    return fernet.encrypt(password.encode())

def get_all_logins():
    cursor.execute("""SELECT * FROM passwords WHERE login != 'root'""")
    return [{'ID': line[0], 'Login':line[1], 'Password': decrypt_password(line[2])} for line in cursor.fetchall()]
