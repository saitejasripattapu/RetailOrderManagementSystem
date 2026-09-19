"""End-to-end tests launch main.py rather than importing application functions."""

import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class OrderEndToEndTests(unittest.TestCase):
    def run_application(self, answers):
        """Each answer is one terminal response followed by Enter."""
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "main.py")],
            input="\n".join(answers) + "\n",
            text=True,
            capture_output=True,
            cwd=PROJECT_ROOT,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def test_01_regular_customer_buys_below_stock(self):
        answers = [
            "1", "Teja", "teja@example.com", "Regular",  # Create customer
            "2", "Notebook", "10.00", "10",              # Create product
            "3", "1", "Notebook", "3", "/done",          # Place order
            "3", "1", "/cancel", "y",                    # Inspect remaining stock
            "0",
        ]
        output = self.run_application(answers)
        self.assertIn("Order created successfully. Order ID: 1.", output)
        self.assertEqual(output.count("Order created successfully."), 1)
        self.assertIn("Customer: Teja (Regular)", output)
        self.assertIn("1 | Notebook | 10.00 | 3 | 30.00", output)
        self.assertIn("Subtotal: 30.00", output)
        self.assertIn("Discount rate: 2%", output)
        self.assertIn("Discount amount: 0.60", output)
        self.assertIn("Final amount: 29.40", output)
        self.assertIn("1 | Notebook | 10.00 | Stock: 7", output)

    def test_02_regular_customer_selects_zero_stock_product(self):
        answers = [
            "1", "Teja", "teja@example.com", "Regular",
            "2", "Notebook", "10.00", "0",
            "3", "1", "Notebook", "/done", "/cancel", "y",
            "3", "1", "/cancel", "y", "0",
        ]
        output = self.run_application(answers)
        self.assertIn("This product is out of stock for this order.", output)
        self.assertIn("Add at least one product before placing the order.", output)
        self.assertNotIn("Order created successfully.", output)
        self.assertNotIn("Final amount:", output)
        self.assertEqual(output.count("1 | Notebook | 10.00 | Stock: 0"), 2)

    def test_03_regular_customer_requests_more_than_stock(self):
        answers = [
            "1", "Teja", "teja@example.com", "Regular",
            "2", "Notebook", "10.00", "5",
            "3", "1", "Notebook", "6", "/cancel", "y",
            "3", "1", "/cancel", "y", "0",
        ]
        output = self.run_application(answers)
        self.assertIn("Insufficient stock. Available for this order: 5.", output)
        self.assertNotIn("Order created successfully.", output)
        self.assertNotIn("Final amount:", output)
        self.assertEqual(output.count("1 | Notebook | 10.00 | Stock: 5"), 2)

    def test_04_regular_customer_selects_unknown_product(self):
        answers = [
            "1", "Teja", "teja@example.com", "Regular",
            "2", "Notebook", "10.00", "10",
            "3", "1", "Unknown product", "/done", "/cancel", "y",
            "3", "1", "/cancel", "y", "0",
        ]
        output = self.run_application(answers)
        self.assertIn("Product not found. Enter an existing product name.", output)
        self.assertIn("Add at least one product before placing the order.", output)
        self.assertNotIn("Order created successfully.", output)
        self.assertNotIn("Final amount:", output)
        self.assertEqual(output.count("1 | Notebook | 10.00 | Stock: 10"), 2)

    def test_05_premium_customer_buys_multiple_products(self):
        answers = [
            "1", "Teja", "teja@example.com", "Premium",
            "2", "Notebook", "10.00", "10",
            "2", "Pen", "2.50", "20",
            "3", "1", "Notebook", "2", "Pen", "4", "/done",
            "3", "1", "/cancel", "y", "0",
        ]
        output = self.run_application(answers)
        self.assertEqual(output.count("Order created successfully."), 1)
        self.assertIn("Customer: Teja (Premium)", output)
        self.assertIn("1 | Notebook | 10.00 | 2 | 20.00", output)
        self.assertIn("2 | Pen | 2.50 | 4 | 10.00", output)
        self.assertIn("Subtotal: 30.00", output)
        self.assertIn("Discount rate: 5%", output)
        self.assertIn("Discount amount: 1.50", output)
        self.assertIn("Final amount: 28.50", output)
        self.assertIn("1 | Notebook | 10.00 | Stock: 8", output)
        self.assertIn("2 | Pen | 2.50 | Stock: 16", output)

    def test_06_corporate_customer_places_multiple_orders(self):
        answers = [
            "1", "Teja", "teja@example.com", "Corporate",
            "2", "Notebook", "10.00", "20",
            "2", "Pen", "2.50", "40",
            "3", "1", "Notebook", "3", "Pen", "4", "/done",  # Order 1
            "3", "1", "Notebook", "2", "Pen", "6", "/done",  # Order 2
            "3", "1", "/cancel", "y", "0",
        ]
        output = self.run_application(answers)
        self.assertEqual(output.count("Order created successfully."), 2)
        # Split the output so each order's amounts are checked independently.
        first, second = output.split("Order created successfully. Order ID: 2.")
        self.assertIn("Order created successfully. Order ID: 1.", first)
        self.assertIn("Customer: Teja (Corporate)", first)
        self.assertIn("1 | Notebook | 10.00 | 3 | 30.00", first)
        self.assertIn("2 | Pen | 2.50 | 4 | 10.00", first)
        self.assertIn("Subtotal: 40.00", first)
        self.assertIn("Discount amount: 2.80", first)
        self.assertIn("Final amount: 37.20", first)
        self.assertIn("Customer: Teja (Corporate)", second)
        self.assertIn("1 | Notebook | 10.00 | 2 | 20.00", second)
        self.assertIn("2 | Pen | 2.50 | 6 | 15.00", second)
        self.assertIn("Subtotal: 35.00", second)
        self.assertIn("Discount amount: 2.45", second)
        self.assertIn("Final amount: 32.55", second)
        self.assertEqual(output.count("Discount rate: 7%"), 2)
        self.assertIn("1 | Notebook | 10.00 | Stock: 15", second)
        self.assertIn("2 | Pen | 2.50 | Stock: 30", second)


if __name__ == "__main__":
    unittest.main()

