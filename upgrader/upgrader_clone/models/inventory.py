from models.db import db
from models.skin import SkinFactory


class Inventory:
    @staticmethod
    def get_user_inventory(user_id):
        cursor = db.cursor()
        cursor.execute("""
            SELECT inventory.id AS inv_id, skins.*
            FROM inventory
            JOIN skins ON inventory.skin_id = skins.id
            WHERE inventory.user_id = %s
            ORDER BY inventory.acquired_at DESC
        """, (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        result = []
        for r in rows:
            skin = SkinFactory.create(r)
            skin.inv_id = r['inv_id']
            result.append(skin)
        return result

    @staticmethod
    def add_item(user_id, skin_id):
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO inventory (user_id, skin_id) VALUES (%s, %s)",
            (user_id, skin_id)
        )
        db.commit()
        inv_id = cursor.lastrowid
        cursor.close()
        return inv_id

    @staticmethod
    def remove_item(inv_id):
        cursor = db.cursor()
        cursor.execute("DELETE FROM inventory WHERE id = %s", (inv_id,))
        db.commit()
        cursor.close()
