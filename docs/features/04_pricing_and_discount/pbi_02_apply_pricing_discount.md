### PBI-02: Apply a Customer Discount

#### User Story

As a retail employee,
I want the application to apply the discount for the order's customer type,
so that the customer receives the appropriate final order amount.

#### Required Fields

- Order subtotal calculated by PBI-01
- Customer type from the order's associated customer

The application obtains these values automatically.

#### Acceptance Criteria

1. Determine the discount rate from the order's customer type:
   Regular 2%, Premium 5%, or Corporate 7%.
2. Apply the rate to the complete subtotal, with no minimum order amount.
3. Use `Decimal` values for the subtotal, rate, discount, and final amount.
4. Calculate the discount as subtotal multiplied by the rate, then round it
   once to two decimal places using `ROUND_HALF_UP`.
5. Calculate the final amount by subtracting the rounded discount from the
   subtotal, so the displayed figures reconcile exactly.
6. An empty order has a discount of 0.00 and a final amount of 0.00.
7. Recalculate from the current subtotal each time. Never apply another
   discount to a previously discounted final amount.
8. Apply customer-specific discount behaviour through a shared method on the
   customer classes, demonstrating polymorphism.
9. If the customer type is missing or unsupported, display an error and do not
   display a calculated discount or final amount. Do not silently assign a rate.
10. Calculating discounts must not change customer details, order items, or stock.

#### Business Rules

| Customer Type | Discount Rate |
|---|---|
| Regular | 2% |
| Premium | 5% |
| Corporate | 7% |

- Discount amount = subtotal × discount rate, rounded to two decimal places.
- Final amount = subtotal − rounded discount amount.
- Example: a Premium subtotal of 10.10 gives an unrounded discount of 0.505,
  a rounded discount of 0.51, and a final amount of 9.59.
- Apply one customer-type discount per order; discounts do not stack.

#### Messages

| Situation | Type | Message |
|---|---|---|
| Customer type is missing or unsupported | Error | Cannot calculate discount. Customer type must be Regular, Premium, or Corporate. |

Discount and final amount display are covered by PBI-03.

#### High-Level Test Scenarios

| ID | Scenario | Expected Result |
|---|---|---|
| PD-01 | Regular customer with subtotal 100.00 | Discount 2.00; final amount 98.00. |
| PD-02 | Premium customer with subtotal 100.00 | Discount 5.00; final amount 95.00. |
| PD-03 | Corporate customer with subtotal 100.00 | Discount 7.00; final amount 93.00. |
| PD-04 | Premium customer with subtotal 10.10 | Discount rounds from 0.505 to 0.51; final amount 9.59. |
| PD-05 | Regular customer with subtotal 0.01 | Discount 0.00; final amount 0.01. |
| PD-06 | Empty order for any supported customer type | Discount and final amount are 0.00. |
| PD-07 | Calculate repeatedly without order changes | Identical results; no compounded discount or stock changes. |
| PD-08 | Add items after a previous calculation | Discount and final amount reflect the new subtotal. |
| PD-09 | Customer type is missing or unsupported | Error displayed; no calculated discount or final amount. |

#### Dependencies

- PBI-01: Calculate an Order Subtotal.
- Customer Management: Assign a Customer Type.

#### Scope

- Manual discounts, coupons, eligibility verification, taxes, and shipping
  charges are not included.
