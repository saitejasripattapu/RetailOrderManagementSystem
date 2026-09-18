"""Data-driven customer tests using unittest and subTest."""

import unittest
from decimal import Decimal

from src.customer import (
    Customer,
    RegularCustomer,
    PremiumCustomer,
    CorporateCustomer,
)


class CustomerTests(unittest.TestCase):
    def test_valid_customer_details(self):
        # Each row contains input values followed by the expected saved values.
        test_cases = [
            (1, "Sai", "sai@example.com", "Sai", "navya@example.com"),
            (2, " Alex Smith ", " alex@example.com ", "Alex Smith", "alex@example.com"),
            (3, "\tSam\n", "\tsam@example.com\n", "Sam", "sam@example.com"),
        ]

        for customer_id, name, email, expected_name, expected_email in test_cases:
            with self.subTest(customer_id=customer_id):
                customer = Customer(customer_id, name, email)

                self.assertEqual(customer.customer_id, customer_id)
                self.assertEqual(customer.name, expected_name)
                self.assertEqual(customer.email, expected_email)

    def test_missing_name_is_rejected(self):
        test_cases = [None, "", "   ", "\t\n"]

        for name in test_cases:
            with self.subTest(name=name):
                with self.assertRaises(ValueError) as error:
                    Customer(1, name, "navya@example.com")

                self.assertEqual(str(error.exception), "Customer name is required.")

    def test_missing_email_is_rejected(self):
        test_cases = [None, "", "   ", "\t\n"]

        for email in test_cases:
            with self.subTest(email=email):
                with self.assertRaises(ValueError) as error:
                    Customer(1, "Navya", email)

                self.assertEqual(str(error.exception), "Customer email is required.")

    def test_invalid_email_format_is_rejected(self):
        test_cases = [
            "invalid-email",
            "navya@example",
            "@example.com",
            "navya@@example.com",
            "nav ya@example.com",
            "navya@example.com extra",
        ]

        for email in test_cases:
            with self.subTest(email=email):
                with self.assertRaises(ValueError) as error:
                    Customer(1, "Navya", email)

                self.assertEqual(
                    str(error.exception),
                    "Enter a valid email address, such as name@example.com.",
                )

    def test_customer_types_and_discount_rates(self):
        # The same test checks all three subclasses.
        test_cases = [
            (RegularCustomer, "Regular", Decimal("0.02")),
            (PremiumCustomer, "Premium", Decimal("0.05")),
            (CorporateCustomer, "Corporate", Decimal("0.07")),
        ]

        for customer_class, expected_type, expected_rate in test_cases:
            with self.subTest(customer_type=expected_type):
                customer = customer_class(1, " Navya ", " navya@example.com ")

                self.assertIsInstance(customer, Customer)
                self.assertEqual(customer.name, "Navya")
                self.assertEqual(customer.email, "navya@example.com")
                self.assertEqual(customer.customer_type, expected_type)
                self.assertEqual(customer.discount_rate(), expected_rate)


if __name__ == "__main__":
    unittest.main()
