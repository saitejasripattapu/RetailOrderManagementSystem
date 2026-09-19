from src.customer import Customer, RegularCustomer, PremiumCustomer, CorporateCustomer
from src.product import Product
from src.order import place_order, display_order


def confirm_product_cancellation(updating):
    message = (
        "Unsaved product changes will be lost. Cancel update? (y/n) "
        if updating else
        "Unsaved product details will be lost. Cancel creation? (y/n) "
    )
    while True:
        answer = input(message).strip().casefold()
        if answer in ("y", "n"):
            return answer == "y"
        print("Enter y or n.")


def enter_product_details(product=None):
    """Keep pending input separate from the saved product."""
    updating = product is not None
    details = {}
    unsaved = False
    print("Enter /cancel to return to the main menu.")
    if updating:
        print("Leave a field blank to keep its current value.")
    for field, validator in (
        ("name", Product.validate_name),
        ("price", Product.validate_price),
        ("stock", Product.validate_stock),
    ):
        while True:
            value = input(f"Product {field}: ")
            if value.strip().casefold() == "/cancel":
                if not unsaved or confirm_product_cancellation(updating):
                    return None
                continue
            if updating and not value.strip():
                details[field] = getattr(product, field)
                break
            try:
                validated = validator(value)
            except ValueError as error:
                unsaved = unsaved or bool(value.strip())
                print(error)
            else:
                details[field] = validated
                unsaved = unsaved or not updating or validated != getattr(product, field)
                break
    return details


def create_customer(customer_id):
    """Validate each field, then create the customer automatically."""
    print("Enter /cancel to cancel customer creation.")
    details = {}
    has_entered_details = False

    for field, validator in (
        ("name", Customer.validate_name),
        ("email", Customer.validate_email),
    ):
        while True:
            value = input(f"Customer {field}: ")
            if value.strip().lower() == "/cancel":
                if not has_entered_details or confirm_customer_cancellation():
                    return None
                continue

            has_entered_details = has_entered_details or bool(value.strip())
            try:
                details[field] = validator(value)
            except ValueError as error:
                print(error)
            else:
                break

    customer_types = {
        "regular": RegularCustomer,
        "premium": PremiumCustomer,
        "corporate": CorporateCustomer,
    }
    while True:
        selected_type = input(
            "Customer type (Regular, Premium, Corporate): "
        ).strip().casefold()
        if selected_type == "/cancel":
            if confirm_customer_cancellation():
                return None
            continue
        if not selected_type:
            print("No customer type selected. Regular will be assigned.")
            selected_type = "regular"

        customer_class = customer_types.get(selected_type)
        if customer_class is None:
            print("Invalid customer type. Choose Regular, Premium, or Corporate.")
            continue
        return customer_class(customer_id, details["name"], details["email"])


def confirm_customer_cancellation():
    while True:
        answer = input(
            "Unsaved customer details will be lost. Cancel creation? (y/n) "
        ).strip().lower()
        if answer == "y":
            return True
        if answer == "n":
            return False
        print("Enter y or n.")


def main():
    """Start the application."""
    # These live for this run only, and are not reset when the menu repeats.
    customers = {}
    next_customer_id = 1
    products = {}
    next_product_id = 1
    orders = {}
    next_order_id = 1

    print("Retail Order Management System")
    while True:
        choice = input(
            "\n1. Create customer\n2. Create product\n3. Place order\n0. Exit\nChoose: "
        ).strip()

        if choice == "1":
            customer = create_customer(next_customer_id)
            if customer is not None:
                duplicate = any(
                    existing.email.casefold() == customer.email.casefold()
                    for existing in customers.values()
                )
                if duplicate:
                    print("A customer with this email already exists.")
                    continue

                customers[customer.customer_id] = customer
                next_customer_id += 1
                print(
                    "Customer created successfully. "
                    f"Customer ID: {customer.customer_id}."
                )
        elif choice == "2":
            details = enter_product_details()
            if details is not None:
                product = Product(next_product_id, **details)
                products[product.product_id] = product
                next_product_id += 1
                print(f"Product created successfully. Product ID: {product.product_id}.")
        elif choice == "3":
            order = place_order(next_order_id, customers, products)
            if order is not None:
                orders[order.order_id] = order
                next_order_id += 1
                print(f"Order created successfully. Order ID: {order.order_id}.")
                display_order(order)
        elif choice == "0":
            break
        else:
            print("Choose 1, 2, 3, or 0.")


if __name__ == "__main__":
    main()
