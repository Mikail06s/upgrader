from models.db import db


class Market:
    @staticmethod
    def get_active_listings():
        cursor = db.cursor()
        cursor.execute("""
            SELECT market_listings.id, market_listings.price, market_listings.created_at,
                   users.username AS seller_name,
                   skins.id AS skin_id, skins.name AS skin_name, skins.image_url, skins.wear
            FROM market_listings
            JOIN users ON market_listings.seller_id = users.id
            JOIN inventory ON market_listings.inventory_id = inventory.id
            JOIN skins ON inventory.skin_id = skins.id
            WHERE market_listings.status = 'active'
            ORDER BY market_listings.created_at DESC
        """)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    @staticmethod
    def create_listing(seller_id, inventory_id, price):
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO market_listings (seller_id, inventory_id, price) VALUES (%s, %s, %s)",
            (seller_id, inventory_id, price)
        )
        db.commit()
        listing_id = cursor.lastrowid
        cursor.close()
        return listing_id

    @staticmethod
    def buy_listing(listing_id, buyer_id):
        cursor = db.cursor()
        cursor.execute("START TRANSACTION")
        try:
            cursor.execute("""
                SELECT seller_id, inventory_id, price, status
                FROM market_listings WHERE id = %s FOR UPDATE
            """, (listing_id,))
            listing = cursor.fetchone()
            if not listing or listing['status'] != 'active':
                cursor.execute("ROLLBACK")
                return False, 'Объявление не найдено или уже продано'

            seller_id = listing['seller_id']
            inventory_id = listing['inventory_id']
            price = float(listing['price'])

            cursor.execute("SELECT balance FROM users WHERE id = %s FOR UPDATE", (buyer_id,))
            buyer = cursor.fetchone()
            if buyer['balance'] < price:
                cursor.execute("ROLLBACK")
                return False, 'Недостаточно средств'

            cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (price, buyer_id))
            cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (price, seller_id))
            cursor.execute("UPDATE inventory SET user_id = %s WHERE id = %s", (buyer_id, inventory_id))
            cursor.execute("UPDATE market_listings SET status = 'sold' WHERE id = %s", (listing_id,))

            cursor.execute("COMMIT")
            return True, 'Покупка успешна!'
        except Exception as e:
            cursor.execute("ROLLBACK")
            return False, str(e)
        finally:
            cursor.close()
