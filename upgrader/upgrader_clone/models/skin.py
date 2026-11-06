from models.db import db


class Skin:
    def __init__(self, row):
        self.id = row['id']
        self.name = row['name']
        self.tier = row['tier']
        self.wear = row['wear']
        self.price = float(row['price'])
        self.image_url = row['image_url']
        self.description = row['description']

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'tier': self.tier,
            'wear': self.wear,
            'price': self.price,
            'image_url': self.image_url,
            'description': self.description,
        }


class SkinFactory:
    """Factory: создаёт объекты Skin из строк БД."""
    @staticmethod
    def create(row):
        return Skin(row)


class SkinModel:
    @staticmethod
    def get_all():
        cursor = db.cursor()
        cursor.execute("SELECT * FROM skins ORDER BY price ASC")
        rows = cursor.fetchall()
        cursor.close()
        return [SkinFactory.create(r) for r in rows]

    @staticmethod
    def get_by_id(skin_id):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM skins WHERE id = %s", (skin_id,))
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return None
        return SkinFactory.create(row)
