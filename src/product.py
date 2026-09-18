"""Products and validation of their details."""

from decimal import Decimal, InvalidOperation


class Product:
    def __init__(self, product_id, name, price, stock):
        self._product_id = product_id
        self.update(name, price, stock)

    @property
    def product_id(self):
        return self._product_id

    @staticmethod
    def validate_name(value):
        if value is None:
            raise ValueError("Product name is required.")

        name = value.strip()
        if name == "":
            raise ValueError("Product name is required.")
        return name

    @staticmethod
    def validate_price(value):
        if value is None:
            raise ValueError("Product price is required.")

        text = str(value).strip()
        if text == "":
            raise ValueError("Product price is required.")
        message = "Enter a price greater than zero with at most two decimal places, such as 19.99."

        # Convert the entered text to an exact decimal number.
        try:
            price = Decimal(text)
        except InvalidOperation:
            raise ValueError(message)

        # Reject special values such as NaN and Infinity before comparing.
        if not price.is_finite():
            raise ValueError(message)
        if price <= 0:
            raise ValueError(message)

        # Decimal records decimal places as a negative exponent:
        # 19.99 has exponent -2; 19.999 has exponent -3.
        decimal_places = -price.as_tuple().exponent
        if decimal_places > 2:
            raise ValueError(message)
        return price

    @staticmethod
    def validate_stock(value):
        if value is None:
            raise ValueError("Stock is required.")

        text = str(value).strip()
        if text == "":
            raise ValueError("Stock is required.")

        # Allow an optional plus sign, then require digits from 0 to 9.
        if text.startswith("+"):
            text = text[1:]
        if not text.isascii() or not text.isdecimal():
            raise ValueError("Enter a whole number greater than or equal to zero.")

        try:
            return int(text)
        except ValueError:
            # Python also rejects integer strings that are excessively long.
            raise ValueError("Enter a whole number greater than or equal to zero.")

    def update(self, name, price, stock):
        """Validate all proposed values before applying any changes."""
        name = self.validate_name(name)
        price = self.validate_price(price)
        stock = self.validate_stock(stock)
        self.name = name
        self.price = price
        self.stock = stock

    def check_availability(self, quantity):
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Enter a whole-number quantity greater than zero.")
        if self.stock == 0:
            raise ValueError("This product is out of stock.")
        if quantity > self.stock:
            raise ValueError(f"Insufficient stock. Stock: {self.stock}.")

    def reduce_stock(self, quantity):
        self.check_availability(quantity)
        self.stock -= quantity
