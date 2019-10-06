

class Item(object):
    def __init__(self, name_id, name, compartment, description, price=10, amount=None):
        self.name_id = name_id  # for example, 'lomsak_apple'
        self.name = name  # for example, 'Lomsak apple'
        self.description = description or f"it's just some {name}"
        self.amount = amount
        self.price = price
        self.compartment = compartment

    def __str__(self):
        return f'{self.name} ({self.name_id})'


"""
    Price of items:
    https://www.numbeo.com/cost-of-living/country_result.jsp?country=Thailand
    1kg of rice: 37.69B
    1 apple: 8B
    1 liter of water: 12B
"""
