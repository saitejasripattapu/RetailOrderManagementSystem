### PBI-03: Display the Final Order Amount

#### User Story

As a retail employee,
I want to view the order subtotal, customer discount, and final amount,
so that I can explain the amount payable to the customer.

#### Required Fields

- Order ID, entered through View an Order

All monetary values are calculated automatically from the selected order.

#### Acceptance Criteria

1. Extend the existing View an Order flow with item amounts and a pricing summary.
   Reuse its order selection, validation, and not-found messages.
2. Display the order ID and the customer's ID, name, and customer type.
3. Display each item's line number, product ID, captured name, captured unit
   price, quantity, and calculated item amount in addition order.
4. After the items, display subtotal, discount rate, discount amount, and final
   amount, using PBI-01 and PBI-02 for calculations.
5. Display every monetary amount with exactly two decimal places and show the
   discount rate as a percentage.
6. The displayed subtotal minus the displayed discount must equal the displayed
   final amount.
7. For an empty order, display "This order has no items." and a summary with
   subtotal, discount amount, and final amount all 0.00. Show the customer's rate.
8. If discount calculation fails because of an invalid customer type, display
   the error from PBI-02 instead of a discount rate, discount amount, or final
   amount. Do not show a misleading zero final amount.
9. Viewing the summary must not change orders, customer details, or product stock.
10. Allow another order selection or return to the main menu.

#### Messages

| Situation | Type | Message |
|---|---|---|
| Subtotal is displayed | Information | Subtotal: {subtotal} |
| Discount rate is displayed | Information | Discount rate: {discount_percentage}% |
| Discount amount is displayed | Information | Discount amount: {discount_amount} |
| Final amount is displayed | Information | Final amount: {final_amount} |
| Order has no items | Information | This order has no items. |

#### Example Display

```text
Order ID: 1
Customer ID: 1
Customer: Alex Smith
Customer type: Premium

Line | Product ID | Product  | Unit price | Quantity | Item amount
1    | 1          | Notebook | 10.00      | 2        | 20.00
2    | 2          | Pen set  | 5.50       | 3        | 16.50

Subtotal: 36.50
Discount rate: 5%
Discount amount: 1.83
Final amount: 34.67
```

#### High-Level Test Scenarios

| ID | Scenario | Expected Result |
|---|---|---|
| FA-01 | View the Premium order in the example | Item amounts 20.00 and 16.50; subtotal 36.50; discount 1.83; final amount 34.67. |
| FA-02 | View an order for each supported customer type | Correct customer type, rate, discount, and final amount displayed. |
| FA-03 | Display whole-number or single-decimal amounts | All monetary values show exactly two decimal places. |
| FA-04 | View an empty order | No-items message, correct customer rate, and monetary totals of 0.00. |
| FA-05 | View an order after adding another item | Summary reflects all current items. |
| FA-06 | Change a product's price after an item was added | Existing item's captured price is used in the display and calculation. |
| FA-07 | View a subtotal whose discount requires rounding | Displayed subtotal minus rounded discount equals displayed final amount. |
| FA-08 | View an order with a missing or unsupported customer type | Discount error; rate, discount amount, and final amount omitted. |
| FA-09 | View repeatedly | Same values; stock and order details unchanged. |
| FA-10 | Return to the main menu | Main menu displayed. |

#### Dependencies

- PBI-01: Calculate an Order Subtotal.
- PBI-02: Apply a Customer Discount.
- Order Management: View an Order.

#### Scope

- All prices use one consistent currency; currency selection and conversion
  are outside this version. No currency symbol is assumed in the display.
- Payment processing, checkout, invoices, taxes, and shipping are not included.
