"""End-to-end tests for placing complete orders by product name."""
import subprocess
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def run_app(answers):
    result = subprocess.run([sys.executable, str(ROOT / 'main.py')],
                            input='\n'.join(answers)+'\n', text=True,
                            capture_output=True, cwd=ROOT, timeout=10)
    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)
    return result.stdout

def setup(kind='Regular', price='10', stock='10'):
    return ['1', 'Alex', 'a@example.com', kind, '2', 'Notebook', price, stock]

class OrderEndToEndTests(unittest.TestCase):
    def test_multiple_products_and_automatic_total(self):
        output=run_app(setup('Premium')+['2','Pen','2.50','20','3','1',
                                       ' notebook ','2','Pen','4','/done','0'])
        for text in ['Order created successfully. Order ID: 1.', 'Subtotal: 30.00',
                     'Discount amount: 1.50','Final amount: 28.50']:
            self.assertIn(text,output)
    def test_retries_repeated_products_and_shared_stock(self):
        output=run_app(setup(stock='5')+['3','1','Missing','Notebook','0','6','3',
                                       'Notebook','3','2','/done',
                                       '3','1','Notebook','/cancel','y','0'])
        self.assertIn('Product not found.',output)
        self.assertIn('Available for this order: 2.',output)
        self.assertIn('Final amount: 49.00',output)
        self.assertIn('This product is out of stock',output)
        self.assertEqual(output.count('Order created successfully.'),1)
    def test_cancel_preserves_stock_and_order_id(self):
        output=run_app(setup(stock='3')+['3','1','Notebook','3','/cancel','y',
                                       '3','1','Notebook','3','/done','0'])
        self.assertIn('Order ID: 1.',output)
        self.assertNotIn('Order ID: 2.',output)
        self.assertIn('Final amount: 29.40',output)
    def test_empty_order_and_declined_cancel(self):
        output=run_app(setup()+['3','1','/done','Notebook','1','/cancel','n','/done','0'])
        self.assertIn('Add at least one product',output)
        self.assertIn('Final amount: 9.80',output)
    def test_duplicate_product_names_require_selection(self):
        output=run_app(setup()+['2','Notebook','20','5','3','1','Notebook','2','1','/done','0'])
        self.assertIn('Several products have this name.',output)
        self.assertIn('Subtotal: 20.00',output)
    def test_multiple_orders_and_restart(self):
        output=run_app(setup('Corporate')+['3','1','Notebook','2','/done',
                                         '3','1','Notebook','3','/done','0'])
        self.assertIn('Order ID: 2.',output)
        self.assertIn('Final amount: 18.60',output)
        self.assertIn('Final amount: 27.90',output)
        self.assertIn('No customers found.',run_app(['3','0']))
