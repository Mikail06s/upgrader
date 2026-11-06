import os
import random
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import check_password_hash

from config import SECRET_KEY, START_BALANCE
from models.db import db               # Singleton — соединение с БД
from models.user import User
from models.skin import SkinModel
from models.inventory import Inventory
from models.market import Market
from models.upgrade import UpgradeStrategy

app = Flask(__name__)
app.secret_key = SECRET_KEY


# ==================== АВТОРИЗАЦИЯ ====================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']

        if User.get_by_username(username):
            flash('Пользователь с таким именем уже существует')
            return redirect(url_for('register'))

        user_id = User.create(username, email, password, START_BALANCE)
        # Дарим стартовый скин (ID 1 = AK-47 Redline)
        starter = SkinModel.get_by_id(1)
        if starter:
            Inventory.add_item(user_id, starter.id)

        flash('Регистрация успешна! Войдите в аккаунт.')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        user = User.get_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        flash('Неверный логин или пароль')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# ==================== ГЛАВНАЯ (КАТАЛОГ СКИНОВ) ====================

@app.route('/')
def index():
    skins = SkinModel.get_all()
    user = None
    balance = 0
    if 'user_id' in session:
        user = User.get_by_id(session['user_id'])
        balance = float(user['balance']) if user else 0
    return render_template('index.html', skins=skins, user=user, balance=balance)


# ==================== ПРОФИЛЬ ====================

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.get_by_id(session['user_id'])
    inventory = Inventory.get_user_inventory(session['user_id'])
    return render_template('profile.html', user=user, balance=float(user['balance']), inventory=inventory)


# ==================== АПГРЕЙД ====================

@app.route('/upgrade', methods=['GET', 'POST'])
def upgrade():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.get_by_id(session['user_id'])
    balance = float(user['balance'])
    inventory = Inventory.get_user_inventory(session['user_id'])
    skins = SkinModel.get_all()

    result = None
    win = None
    chance = 0
    cost = 0
    target_skin = None

    if request.method == 'POST':
        input_inv_id = int(request.form['input_inv_id'])
        output_skin_id = int(request.form['output_skin_id'])
        cost = float(request.form['cost'])

        output_obj = SkinModel.get_by_id(output_skin_id)
        output_price = output_obj.price if output_obj else 1

        # Шанс считаем через Стратегию (входная цена aproximately 5000)
        input_price = 5000.0
        chance = UpgradeStrategy.calculate_chance(input_price, output_price)
        win = UpgradeStrategy.roll(chance)

        if balance >= cost:
            if win:
                new_balance = balance - cost + output_price
                User.set_balance(session['user_id'], new_balance)
                Inventory.add_item(session['user_id'], output_skin_id)
                Inventory.remove_item(input_inv_id)
                result = f'ПОБЕДА! Вы получили {output_obj.name}!'
                win = True
                target_skin = output_obj
            else:
                new_balance = balance - cost
                User.set_balance(session['user_id'], new_balance)
                Inventory.remove_item(input_inv_id)
                result = 'Проигрыш. Скина сгорела.'
                win = False
        else:
            result = 'Недостаточно средств на балансе.'
            win = False

    return render_template(
        'upgrade.html',
        user=user, balance=balance, inventory=inventory, skins=skins,
        result=result, win=win, chance=chance, cost=cost, target_skin=target_skin
    )


# ==================== МАРКЕТ / ТОРГОВЛЯ ====================

@app.route('/market')
def market():
    listings = Market.get_active_listings()
    user = None
    balance = 0
    if 'user_id' in session:
        user = User.get_by_id(session['user_id'])
        balance = float(user['balance'])
    return render_template('market.html', listings=listings, user=user, balance=balance)


@app.route('/market/sell', methods=['POST'])
def market_sell():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    inv_id = int(request.form['inv_id'])
    price = float(request.form['price'])
    Market.create_listing(session['user_id'], inv_id, price)
    flash('Скина выставлена на продажу!')
    return redirect(url_for('profile'))


@app.route('/market/buy/<int:listing_id>')
def market_buy(listing_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    success, msg = Market.buy_listing(listing_id, session['user_id'])
    flash(msg)
    return redirect(url_for('market'))


# ==================== API БАЛАНС (AJAX) ====================

@app.route('/api/balance')
def api_balance():
    if 'user_id' not in session:
        return jsonify({'balance': 0})
    user = User.get_by_id(session['user_id'])
    return jsonify({'balance': float(user['balance']) if user else 0})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
