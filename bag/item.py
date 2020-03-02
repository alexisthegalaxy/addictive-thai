import sqlite3


CONN = sqlite3.connect("thai.db")
CURSOR = CONN.cursor()


class Item(object):
    def __init__(self, name_id, name=None, description=None, price=10, amount=1):
        self.name_id = name_id  # for example, 'lomsak_apple'
        if not name:
            item = list(
                CURSOR.execute(
                    f"""
                    SELECT name, description, price
                    FROM items
                    WHERE id = '{name_id}'
                    """
                )
            )[0]
            self.name = item[0]
            self.description = item[1]
            self.price = item[2]
            self.amount = amount
        else:
            self.name = name  # for example, 'Lomsak apple'
            self.description = description or f"it's just some {name}"
            self.amount = amount
            self.price = price

    def __str__(self):
        return f'{self.name} ({self.name_id})'


"""
    Price of items:
    https://www.numbeo.com/cost-of-living/country_result.jsp?country=Thailand
    1kg of rice: 37.69B
    1 apple: 8B
    1 liter of water: 12B
"""
