"""Product validation and command-line workflows."""

import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from io import StringIO
from unittest.mock import patch

from main import enter_product_details
from src.product import Product


class ProductTests(unittest.TestCase):
    def run_flow(self, function, inputs, *args):
        output = StringIO()
        with patch("builtins.input", side_effect=inputs), redirect_stdout(output):
            result = function(*args)
        return result, output.getvalue()

    def test_valid_details_are_trimmed_and_converted(self):
        product = Product(1, " Pen ", " 5.50 ", " 0 ")
        self.assertEqual((product.name, product.price, product.stock),
                         ("Pen", Decimal("5.50"), 0))

    def test_invalid_details(self):
        cases = (
            (Product.validate_name, [None, "", "  "]),
            (Product.validate_price, [None, "", "bad", "0", "-1", "NaN",
                                      "Infinity", "1.001", "1.000"]),
            (Product.validate_stock, [None, "", "bad", "-1", "1.5", True]),
        )
        for validator, values in cases:
            for value in values:
                with self.subTest(validator=validator.__name__, value=value):
                    with self.assertRaises(ValueError):
                        validator(value)

    def test_update_validates_before_mutation(self):
        product = Product(1, "Pen", "5", 10)
        with self.assertRaises(ValueError):
            product.update("New name", "bad", 4)
        self.assertEqual((product.name, product.price, product.stock),
                         ("Pen", Decimal("5"), 10))
        product.update("New name", "6.50", 4)
        self.assertEqual(product.stock, 4)
        with self.assertRaises(AttributeError):
            product.product_id = 2

    def test_create_retry_and_decline_cancellation(self):
        details, _ = self.run_flow(enter_product_details,
                                  [" Pen ", "bad", "/cancel", "n", "5.5", "0"])
        self.assertEqual(details, {"name": "Pen", "price": Decimal("5.5"), "stock": 0})

    def test_cancel_create(self):
        result, _ = self.run_flow(enter_product_details, ["Pen", "/cancel", "y"])
        self.assertIsNone(result)



if __name__ == "__main__":
    unittest.main()
