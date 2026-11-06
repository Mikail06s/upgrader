from models.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    @staticmethod
    def create(username, email, password, balance=5000.00):
        cursor = db.cursor()
        hashed = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, balance) VALUES (%s, %s, %s, %s)",
            (username, email, hashed, balance)
        )
        db.commit()
        user_id = cursor.lastrowid
        cursor.close()
        return user_id

    @staticmethod
    def get_by_username(username):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
        cursor.close()
        return row

    @staticmethod
    def get_by_id(user_id):
        cursor = db.cursor()
        cursor.execute("SELECT id, username, email, balance, created_at FROM users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        cursor.close()
        return row

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return check_password_hash(hashed_password, plain_password)

    @staticmethod
    def add_balance(user_id, amount):
        cursor = db.cursor()
        cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, user_id))
        db.commit()
        cursor.close()

    @staticmethod
    def set_balance(user_id, amount):
        cursor = db.cursor()
        cursor.execute("UPDATE users SET balance = %s WHERE id = %s", (amount, user_id))
        db.commit()
        cursor.close()
