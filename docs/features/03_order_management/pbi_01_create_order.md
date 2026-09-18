### PBI-01: Create an Order

#### User Story

As a retail employee,
I want to create an order for an existing customer,
so that I can add products to their order during the current session.

#### Required Fields

- Customer ID

#### Acceptance Criteria

1. Allow the employee to view customers before entering a customer ID.
2. Customer ID is mandatory. Trim surrounding whitespace and reject blank
   or non-integer input.
3. The customer ID must identify a customer in the current session.
4. If validation fails, display the relevant error and allow correction.
   Do not create an order.
5. If no customers exist, display "No customers found. Create a customer first."
   and allow return to the main menu.
6. Generate a unique order ID within the current session.
7. Store the order ID, associated customer, and an initially empty collection
   of order items in memory.
8. Allow multiple orders for the same customer.
9. Display success only after the order is stored. Creating an empty order
   does not change product stock.
10. Allow the employee to proceed to adding products or return to the main menu.
11. Orders remain available during the current session. Restarting the
    application clears all orders.

#### In-Memory Storage Requirements

| Field | Constraint |
|---|---|
| order_id | Automatically generated, non-null, and unique within the session |
| customer | Required; references an existing customer with a valid customer type |
| items | Initially empty; contains the order's items |

#### Messages

| Situation | Type | Message |
|---|---|---|
| Customer ID is missing or blank | Error | Customer ID is required. |
| Customer ID is not an integer | Error | Enter a valid whole-number customer ID. |
| Customer ID does not exist | Error | Customer not found. Enter an existing customer ID. |
| No customers exist | Information | No customers found. Create a customer first. |
| Order is successfully created | Success | Order created successfully. Order ID: {order_id}. |
| Employee cancels after entering details | Warning | Unsaved order details will be lost. Cancel creation? (y/n) |

#### Cancellation Behaviour

- If the employee confirms cancellation before creation, discard the entered
  details and return to the main menu without creating an order.
- Otherwise, retain the entered details and continue entry.
- Returning to the main menu after successful creation keeps the order.

#### High-Level Test Scenarios

| ID | Scenario | Expected Result |
|---|---|---|
| CO-01 | Submit an existing customer ID | Empty order created for that customer; generated order ID displayed. |
| CO-02 | Submit a blank or whitespace-only customer ID | Required-field error; no order created. |
| CO-03 | Submit a non-integer customer ID | Invalid-ID error; correction allowed. |
| CO-04 | Submit an unknown customer ID | Customer-not-found error; no order created. |
| CO-05 | Create an order when no customers exist | No-customers message; return to main menu available. |
| CO-06 | Submit a valid ID with surrounding whitespace | Whitespace removed; order created. |
| CO-07 | Create multiple orders for one customer | Each order has a distinct ID and its own empty item collection. |
| CO-08 | Create an empty order | Product stock remains unchanged. |
| CO-09 | Confirm cancellation before creation | Details discarded; no order created. |
| CO-10 | Decline cancellation | Details retained; entry continues. |
| CO-11 | Return to the menu after creation | Order remains available during the session. |
| CO-12 | Restart the application | Order collection is empty. |

#### Dependencies

- Customer Management: Create a Customer, View Customers, and Assign a Customer Type.

#### Scope

- Adding products is covered by PBI-02.
- Changing the customer, deleting orders, and cancelling stored orders are
  outside this PBI.
