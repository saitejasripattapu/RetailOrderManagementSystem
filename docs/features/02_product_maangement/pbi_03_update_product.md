### PBI-03: Update a Product

#### User Story

As a retail employee,
I want to update a product's name, price, and stock,
so that its details remain accurate during the current session.

#### Required Fields

- Product ID (to select an existing product)

The following fields can be updated. Blank input keeps the current value:

- Name
- Price
- Stock

#### Acceptance Criteria

1. Select an existing product using its product ID.
2. Remove leading and trailing whitespace from input before validation.
3. Reject a missing or non-integer product ID and allow correction.
4. If the product ID does not exist, display an error and allow another selection.
5. If no products exist, display:
   "No products found. Create a product first."
   Allow the employee to return to the main menu.
6. Display the selected product's current ID, name, price, and stock
   before editing. Display the price with two decimal places.
7. Allow the employee to update the name, price, stock, or any
   combination of these fields. The product ID cannot be changed.
8. Empty or whitespace-only input for an editable field keeps its current value.
   Stored names cannot be null or blank.
9. A new price must be a finite number greater than zero, with at most two
   decimal places.
10. A new stock must be a whole number greater than or equal to zero.
    Reject nonnumeric, negative, or fractional quantities.
11. The entered quantity replaces the current stock; it is not
    added to the current quantity.
12. If any new value is invalid, display the relevant error and allow correction.
    Do not apply any changes until all new values are valid and submitted.
13. Update the existing product in memory without creating another product or
    changing other products.
14. Display success only after the changes have been applied. If all values
    remain unchanged, display "No changes made." instead.
15. Updated details are visible when viewing products in the current session.
    Restarting the application clears all products.
16. Allow cancellation and return to the main menu.

#### In-Memory Storage Requirements

| Field | Constraint |
|---|---|
| product_id | Must identify an existing product; cannot be changed |
| name | Cannot be null or blank; blank input retains the current name |
| price | Finite, greater than zero, and at most two decimal places; blank input retains the current price |
| stock | Whole number greater than or equal to zero; blank input retains the current quantity |

Keep proposed changes separate from the stored product until validation and
submission are complete.

#### Messages

| Situation | Type | Message |
|---|---|---|
| Product ID is missing or blank | Error | Product ID is required. |
| Product ID is not an integer | Error | Enter a valid whole-number product ID. |
| Product ID does not exist | Error | Product not found. Enter an existing product ID. |
| No products exist | Information | No products found. Create a product first. |
| Price is invalid | Error | Enter a price greater than zero with at most two decimal places, such as 19.99. |
| Stock is invalid | Error | Enter a whole number greater than or equal to zero. |
| Product is successfully updated | Success | Product updated successfully. Product ID: {product_id}. |
| Submitted values leave the product unchanged | Information | No changes made. |
| Employee cancels with unsaved changes | Warning | Unsaved product changes will be lost. Cancel update? (y/n) |

#### Cancellation Behaviour

- If the employee confirms cancellation, discard proposed changes and return
  to the main menu. The stored product remains unchanged.
- Otherwise, return to editing with the entered details retained.
- If there are no unsaved changes, return to the main menu without a warning.

#### High-Level Test Scenarios

| ID | Scenario | Expected Result |
|---|---|---|
| UP-01 | Select an existing product | Current ID, name, price, and stock are displayed. |
| UP-02 | Submit a missing or blank product ID | ID-required error; selection can be corrected. |
| UP-03 | Submit a non-integer product ID | Invalid-ID error; selection can be corrected. |
| UP-04 | Submit an ID that does not exist | Product-not-found error; no product changed. |
| UP-05 | Attempt an update when no products exist | No-products message; return to the main menu is available. |
| UP-06 | Update only the name | Name changes; price, quantity, and ID remain unchanged. |
| UP-07 | Update only the price | Price changes; name, quantity, and ID remain unchanged. |
| UP-08 | Change stock from 10 to 4 | Quantity becomes 4, not 14; other details remain unchanged. |
| UP-09 | Set stock to zero | Product remains stored with zero stock. |
| UP-10 | Update all editable fields with valid values | All changes are applied together; ID remains unchanged. |
| UP-11 | Leave an editable field empty or whitespace-only | That field retains its current value. |
| UP-12 | Leave all fields blank or submit their existing values | No-changes message; product remains unchanged. |
| UP-13 | Submit valid values with surrounding whitespace | Surrounding whitespace removed before changes are applied. |
| UP-14 | Submit a nonnumeric, zero, negative, non-finite, or overly precise price | Invalid-price error; no changes applied. |
| UP-15 | Submit a negative, fractional, or nonnumeric quantity | Invalid-quantity error; no changes applied. |
| UP-16 | Submit a valid name together with an invalid price | Neither change is applied; correction is allowed. |
| UP-17 | Correct invalid input and submit valid changes | Product updated; success message displayed. |
| UP-18 | Confirm cancellation with unsaved changes | Proposed changes discarded; stored product unchanged. |
| UP-19 | Decline cancellation | Entered details retained; editing continues. |
| UP-20 | View products after updating in the same session | Updated details are displayed; other products remain unchanged. |
| UP-21 | Restart after updating a product | Product collection is empty. |

#### Dependencies

- PBI-01: Create a Product.
- PBI-02: View Products displays the updated details.

#### Notes

- Use Python's `Decimal` to represent prices.
- Product name uniqueness has not yet been decided.
- Stock changes when processing orders are covered by Order Management.
- The effect of product updates on existing order items must be defined in
  Order Management.

#### Scope

- Product deletion and stock adjustment history are not included.
