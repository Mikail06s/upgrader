# Настройки подключения к MySQL
# ВНИМАНИЕ: впиши сюда свои данные от MySQL ниже!
DB_CONFIG = {
    'host': 'localhost',        # обычно оставляй localhost
    'user': 'root',             # твой пользователь MySQL (по умолчанию root)
    'password': '',             # <-- ВПИШИ СЮДА СВОЙ ПАРОЛЬ MySQL
    'database': 'upgrader_db',  # имя базы данных
    'port': 3306,
}

SECRET_KEY = 'super-secret-key-change-me'  # ключ для сессий Flask
START_BALANCE = 5000.00           # стартовый баланс в рублях
