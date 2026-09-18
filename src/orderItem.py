"""Orders own immutable snapshots of the products added to them."""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from src.product import Product


@dataclass(frozen=True)
class OrderItem:
    product_id: int
    product_name: str
    unit_price: Decimal
    quantity: int

    def amount(self):
        return self.unit_price * self.quantity

    def __post_init__(self):
        Product.validate_name(self.product_name)
        Product.validate_price(self.unit_price)
        if type(self.quantity) is not int or self.quantity <= 0:
            raise ValueError("Enter a whole-number quantity greater than zero.")


class Order:
    def __init__(self, order_id, customer):
        if getattr(customer, "customer_type", None) not in ("Regular", "Premium", "Corporate"):
            raise ValueError("Customer type must be Regular, Premium, or Corporate.")
        self._order_id = order_id
        self._customer = customer
        self._items = []

    @property
    def order_id(self):
        return self._order_id

    @property
    def customer(self):
        return self._customer

    @property
    def items(self):
        return tuple(self._items)

    def subtotal(self):
        return sum((item.amount() for item in self._items), Decimal("0.00"))

    def pricing_summary(self):
        """Calculate fresh totals; round the discount once before subtraction."""
        if getattr(self.customer, "customer_type", None) not in (
            "Regular", "Premium", "Corporate"
        ):
            raise ValueError(
                "Cannot calculate discount. Customer type must be Regular, Premium, or Corporate."
            )
        # Each customer subclass supplies its own rate (polymorphism).
        rate = self.customer.discount_rate()
        subtotal = self.subtotal()
        discount = (subtotal * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return {
            "subtotal": subtotal,
            "rate": rate,
            "discount": discount,
            "final_amount": subtotal - discount,
        }

    def add_product(self, product, quantity):
        product.check_availability(quantity)
        item = OrderItem(product.product_id, product.name, product.price, quantity)
        # Prepare the new collection before changing either stored object.
        new_items = self._items + [item]
        product.reduce_stock(quantity)
        self._items = new_items

    def place_products(self, selections):
        """Prepare the complete order before committing stock changes."""
        if self._items or not selections:
            raise ValueError("A new order must contain at least one product.")
        totals = {}
        items = []
        for product, quantity in selections:
            item = OrderItem(product.product_id, product.name, product.price, quantity)
            items.append(item)
            totals[product] = totals.get(product, 0) + quantity
        for product, quantity in totals.items():
            product.check_availability(quantity)
        previous_stock = {product: product.stock for product in totals}
        self._items = items
        try:
            self.pricing_summary()
            for product, quantity in totals.items():
                product.reduce_stock(quantity)
        except Exception:
            self._items = []
            for product, stock in previous_stock.items():
                product.stock = stock
            raise
