"""Pricing through the complete order placement flow."""
import unittest
from tst.unittest.test_order import run_app, setup

class PricingEndToEndTests(unittest.TestCase):
    def test_rates_and_rounding(self):
        for kind, price, expected in [('Regular','100','98.00'),
                                       ('Premium','100','95.00'),
                                       ('Corporate','100','93.00'),
                                       ('Premium','10.10','9.59'),
                                       ('Regular','0.01','0.01')]:
            with self.subTest(kind=kind,price=price):
                output=run_app(setup(kind,price)+['3','1','Notebook','1','/done','0'])
                self.assertIn('Final amount: '+expected,output)
