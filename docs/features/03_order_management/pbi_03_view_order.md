### PBI-03: View an Order

#### User Story

As a retail employee,
I want to view an order and its items,
so that I can review the customer's selected products and quantities.

#### Required Fields

- Order ID

#### Acceptance Criteria

1. Allow viewing existing order IDs and associated customer IDs and names
   before selecting an order.
2. Order ID is mandatory. Trim surrounding whitespace and reject blank or
   non-integer input.
3. Retrieve the selected order from the current session's in-memory collection.
   If it does not exist, display an error and allow another selection.
4. Display the order ID and the customer's ID, name, and customer type.
5. Display each item's line number, product ID, captured product name, captured
   unit price, and quantity, in the order items were added.
6. Number lines starting at 1 within the displayed order. Keep repeated product
   additions visible as separate lines.
7. Display unit prices with two decimal places.
8. For an empty order, display its customer details and "This order has no items."
9. If no orders exist, display "No orders found. Create an order first."
10. Viewing must not change order details, items, or product stock.
11. Allow another order selection or return to the main menu.

#### Messages

| Situation | Type | Message |
|---|---|---|
| Order ID is missing or blank | Error | Order ID is required. |
| Order ID is not an integer | Error | Enter a valid whole-number order ID. |
| Order does not exist | Error | Order not found. Enter an existing order ID. |
| No orders exist | Information | No orders found. Create an order first. |
| Selected order has no items | Information | This order has no items. |

#### High-Level Test Scenarios

| ID | Scenario | Expected Result |
|---|---|---|
| VO-01 | View an order with one item | Correct order, customer, and item details displayed. |
| VO-02 | View an order with several items | All lines displayed in addition order, numbered from 1. |
| VO-03 | View repeated additions of one product | Separate lines displayed with their own quantities and captured prices. |
| VO-04 | View an empty order | Customer details and no-items message displayed. |
| VO-05 | View when no orders exist | No-orders message displayed. |
| VO-06 | Submit a blank or non-integer ID | Relevant validation error; correction allowed. |
| VO-07 | Submit an unknown order ID | Order-not-found error; another selection allowed. |
| VO-08 | Submit an existing ID with surrounding whitespace | Correct order displayed. |
| VO-09 | View an item after its product's name or price changes | Captured item name and price displayed. |
| VO-10 | View unit prices of 5 and 5.5 | Displayed as 5.00 and 5.50. |
| VO-11 | Check order and stock after viewing | All stored details remain unchanged. |
| VO-12 | Return to the main menu | Main menu displayed. |
| VO-13 | Restart and attempt to view orders | No-orders message displayed. |

#### Dependencies

- PBI-01: Create an Order.
- PBI-02: Add Products to an Order.

#### Scope

- Item amounts, subtotal, discount, and final total display will be specified
  by the Pricing and Discounts feature.
- Editing, deleting, and filtering orders are not included.
