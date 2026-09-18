### PBI-01: Calculate an Order Subtotal

#### User Story

As a retail employee,
I want to calculate each order item's amount and the order subtotal,
so that I know the total before applying a customer discount.

#### Required Fields

- Existing order, selected through View an Order
- Captured unit price and quantity for each order item

These values come from the stored order; the employee does not enter amounts.

#### Acceptance Criteria

1. Calculate each item's amount as its captured unit price multiplied by its
   quantity.
2. Calculate the subtotal as the sum of all item amounts, including separate
   lines for repeated additions of the same product.
3. Use Python's `Decimal` for monetary calculations; do not use binary floats.
4. Use the prices captured when items were added, regardless of later product
   price changes.
5. An empty order has a subtotal of 0.00.
6. Calculate using all currently stored items whenever an order is viewed,
   including items added since the previous calculation.
7. Calculating amounts must not change items, quantities, prices, or stock.
8. Display item amounts and subtotal with two decimal places as part of PBI-03.

#### Business Rules

- Item amount = captured unit price × quantity.
- Order subtotal = sum of item amounts.
- Unit prices have at most two decimal places and quantities are whole numbers,
  so item multiplication does not require fractional-cent rounding.
- Discounts are applied after calculating the subtotal.

#### Messages

| Situation | Type | Message |
|---|---|---|
| Subtotal is displayed | Information | Subtotal: {subtotal} |

Order selection errors use the messages defined in Order Management's
View an Order PBI.

#### High-Level Test Scenarios

| ID | Scenario | Expected Result |
|---|---|---|
| OS-01 | One item priced 19.99 with quantity 3 | Item amount and subtotal are 59.97. |
| OS-02 | Items priced 10.00 × 2 and 5.50 × 3 | Item amounts are 20.00 and 16.50; subtotal is 36.50. |
| OS-03 | Same product appears on multiple lines | Every line contributes once to the subtotal. |
| OS-04 | Calculate an empty order | Subtotal is 0.00. |
| OS-05 | Change a product price after adding an item | Calculation uses the item's captured price. |
| OS-06 | Add another item and view the order again | Subtotal includes the new item. |
| OS-07 | Calculate 0.10 × 3 | Result is exactly 0.30. |
| OS-08 | Calculate repeatedly without changing the order | Same result; order and stock remain unchanged. |

#### Dependencies

- Order Management: Add Products to an Order and View an Order.

#### Scope

- Customer discounts are covered by PBI-02.
- Taxes, shipping charges, and currency conversion are not included.
