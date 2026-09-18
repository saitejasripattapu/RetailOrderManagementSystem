"""Place a complete order by product name and show its price automatically."""
from orderItem import Order


def confirm_cancel():
    while True:
        answer = input('Discard this order? (y/n) ').strip().lower()
        if answer in ('y', 'n'):
            return answer == 'y'
        print('Enter y or n.')


def place_order(order_id, customers, products):
    if not customers:
        print('No customers found. Create a customer first.')
        return None
    if not products:
        print('No products found. Create a product first.')
        return None
    for customer in customers.values():
        print(f'{customer.customer_id} | {customer.name} | {customer.customer_type}')
    while True:
        value = input('Customer ID (/cancel to return): ').strip()
        if value.lower() == '/cancel':
            return None
        try:
            customer = customers[int(value)]
        except (ValueError, KeyError):
            print('Enter an existing customer ID.')
            continue
        break

    pending = []
    reserved = {}
    print('Enter product names and quantities. Enter /done to place the order or /cancel to discard it.')
    for product in products.values():
        print(f'{product.product_id} | {product.name} | {product.price:.2f} | Stock: {product.stock}')
    while True:
        name = input('Product name (/done to finish): ').strip()
        if name.lower() == '/cancel':
            if confirm_cancel():
                return None
            continue
        if name.lower() == '/done':
            if not pending:
                print('Add at least one product before placing the order.')
                continue
            order = Order(order_id, customer)
            order.place_products(pending)
            return order
        matches = [p for p in products.values() if p.name.casefold() == name.casefold()]
        if not matches:
            print('Product not found. Enter an existing product name.')
            continue
        if len(matches) > 1:
            print('Several products have this name. Select the product ID:')
            for product in matches:
                print(f'{product.product_id} | {product.name} | {product.price:.2f} | Stock: {product.stock}')
            while True:
                value = input('Product ID (/back to product names): ').strip()
                if value == '/back':
                    break
                product = next((p for p in matches if str(p.product_id) == value), None)
                if product is not None:
                    break
                print('Choose one of the displayed product IDs.')
            if value == '/back':
                continue
        else:
            product = matches[0]
        available = product.stock - reserved.get(product.product_id, 0)
        if available == 0:
            print('This product is out of stock for this order.')
            continue
        while True:
            value = input('Quantity (/back to product names, /cancel to discard): ').strip()
            if value.lower() == '/back':
                break
            if value.lower() == '/cancel':
                if confirm_cancel():
                    return None
                continue
            try:
                quantity = int(value)
                if quantity <= 0:
                    raise ValueError
            except ValueError:
                print('Enter a whole-number quantity greater than zero.')
                continue
            if quantity > available:
                print(f'Insufficient stock. Available for this order: {available}.')
                continue
            pending.append((product, quantity))
            reserved[product.product_id] = reserved.get(product.product_id, 0) + quantity
            print(f'Added {quantity} x {product.name} to the pending order.')
            break


def display_order(order):
    print(f'Order ID: {order.order_id}')
    print(f'Customer: {order.customer.name} ({order.customer.customer_type})')
    print('Line | Product | Unit price | Quantity | Item amount')
    for line, item in enumerate(order.items, 1):
        print(f'{line} | {item.product_name} | {item.unit_price:.2f} | {item.quantity} | {item.amount():.2f}')
    summary = order.pricing_summary()
    print(f"Subtotal: {summary['subtotal']:.2f}")
    print(f"Discount rate: {summary['rate'] * 100:.0f}%")
    print(f"Discount amount: {summary['discount']:.2f}")
    print(f"Final amount: {summary['final_amount']:.2f}")
