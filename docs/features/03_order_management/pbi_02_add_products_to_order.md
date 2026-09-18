
#### User Story

As a retail employee,
I want to add products with quantities to an existing order,
so that the order records the items the customer wants to purchase.

#### Required Fields

- Order ID
- Product ID
- Quantity

#### Acceptance Criteria

1. Select an existing order using its order ID. Allow viewing order IDs and
   their associated customers before selection.
2. Allow viewing products, prices, and stock before selecting
   a product by ID.
3. All required fields are mandatory. Trim surrounding whitespace and reject
   blank or non-integer input.
4. Order ID and product ID must identify existing records in the current session.
5. Quantity must be a whole number greater than zero and must not exceed the
   product's current stock.
6. Reject products with zero stock.
7. If validation fails, display the relevant error and allow correction.
   Leave both the order and stock unchanged.
8. On successful submission, append a new order item containing the product ID,
   a copy of its current name and unit price, and the requested quantity.
9. Reduce the product's stock by the submitted quantity only when
   the item is successfully added. Apply both changes together, or neither.
10. Each successful addition creates a separate line, including repeated
    additions of the same product. Validate each addition against remaining stock.
11. Later changes to a product's name or price do not change existing order items.
    A later addition uses the product's name and price at that time.
12. Display success only after the item and stock changes are applied.
13. Allow another addition or return to the main menu. Previously added items
    remain stored when the employee leaves this flow.
14. If no orders or products exist, display the corresponding message and allow
    return to the main menu.
15. Orders, items, and stock exist only during the current session.

#### In-Memory Storage Requirements

| Field | Constraint |
|---|---|
| product_id | Identifies the selected product |
| product_name | Copy of the product name when the item is added |
| unit_price | Copy of the product price when added; stored as `Decimal` |
| quantity | Whole number greater than zero |

Each item belongs to one order's item collection. Stock is held
on the product and must never become negative through an order addition.

#### Messages

| Situation | Type | Message |
|---|---|---|
| Required field is missing or blank | Error | {field_name} is required. |
| Order ID or product ID is not an integer | Error | Enter a valid whole-number {field_name}. |
| Order does not exist | Error | Order not found. Enter an existing order ID. |
| Product does not exist | Error | Product not found. Enter an existing product ID. |
| No orders exist | Information | No orders found. Create an order first. |
| No products exist | Information | No products found. Create a product first. |
| Quantity is nonnumeric, fractional, zero, or negative | Error | Enter a whole-number quantity greater than zero. |
| Product has zero stock | Error | This product is out of stock. |
| Quantity exceeds available stock | Error | Insufficient stock. Stock: {stock}. |
| Item is successfully added | Success | Product added successfully. Order ID: {order_id}. |
| Employee cancels with an unsubmitted addition | Warning | Unsaved item details will be lost. Cancel addition? (y/n) |

#### Cancellation Behaviour

- Confirming cancellation discards only the unsubmitted addition and leaves
  stock unchanged. Previously added items remain in the order.
- Declining cancellation retains entered details and continues entry.
- Returning to the main menu between additions requires no warning.

#### High-Level Test Scenarios

| ID | Scenario | Expected Result |
|---|---|---|
| AO-01 | Add quantity 3 when stock is 10 | One item with quantity 3 added; stock becomes 7. |
| AO-02 | Submit a blank required field | Required-field error; order and stock unchanged. |
| AO-03 | Submit a non-integer order or product ID | Invalid-ID error; correction allowed. |
| AO-04 | Submit an unknown order or product ID | Relevant not-found error; nothing changed. |
| AO-05 | Submit zero, negative, fractional, or nonnumeric quantity | Quantity error; nothing changed. |
| AO-06 | Request more than available stock | Insufficient-stock error showing current availability; nothing changed. |
| AO-07 | Select a product with zero stock | Out-of-stock error; no item added. |
| AO-08 | Request exactly the stock | Item added; stock becomes zero. |
| AO-09 | Add the same product twice | Separate lines created; stock reduced for each successful addition. |
| AO-10 | Repeated addition exceeds remaining stock | Later addition rejected; previous items and remaining stock unchanged. |
| AO-11 | Change product name and price after adding an item | Existing item retains its captured name and price; a new addition uses updated values. |
| AO-12 | Confirm cancellation before submission | Pending details discarded; previous items and stock unchanged. |
| AO-13 | Decline cancellation | Details retained; entry continues. |
| AO-14 | Enter valid values with surrounding whitespace | Whitespace removed; addition succeeds. |
| AO-15 | Enter the flow with no orders or no products | Corresponding message; return to main menu available. |
| AO-16 | Correct invalid input and submit | Item added once; stock reduced once. |
| AO-17 | Add a product to one of several orders | Only the selected order changes; shared product stock decreases. |

#### Dependencies

- PBI-01: Create an Order.
- Product Management: Create a Product and View Products.

#### Notes

- Stock is reduced at successful addition; this version has no checkout step.
- Updating stock through Product Management replaces the remaining
  stock value and does not change quantities already recorded in orders.
- Item amounts, discounts, and order totals are covered by Pricing and Discounts.

#### Scope

- Removing items, editing item quantities, stock restoration, and cancelling
  stored orders are not included.
