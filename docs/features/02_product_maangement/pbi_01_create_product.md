### PBI-01: Create a Product

#### User Story
As a retail employee,
I want to record and save a product's name, price, and stock,
so that the product can be added to orders during the current session.

#### Required Fields
- Name
- Price
- Stock

#### Acceptance Criteria
1. Name, price, and stock are mandatory.
2. Remove leading and trailing whitespace before validation and saving.
3. Reject null, empty, or whitespace-only values.
4. Price must be a finite number greater than zero, with at most two
   decimal places.
5. Stock must be a whole number greater than or equal to zero.
   Reject nonnumeric, negative, or fractional quantities.
6. If validation fails, display the relevant error and allow correction.
   Do not save the product.
7. The application automatically generates a unique product ID within
   the current session.
8. Store the product ID, name, price, and stock together in memory.
9. Display success only after the product is added to the in-memory collection.
10. Products remain available during the current session. Restarting the
   application clears all products.

#### In-Memory Storage Requirements
| Field | Constraint |
|---|---|
| product_id | Automatically generated, non-null, and unique within the session |
| name | Required; cannot be null or blank |
| price | Required; finite, greater than zero, and at most two decimal places |
| stock | Required; whole number greater than or equal to zero |

The application validates product details before adding them to the collection.

#### Messages
| Situation | Type | Message |
|---|---|---|
| Name is missing or blank | Error | Product name is required. |
| Price is missing or blank | Error | Product price is required. |
| Price is invalid | Error | Enter a price greater than zero with at most two decimal places, such as 19.99. |
| Stock is missing or blank | Error | Stock is required. |
| Stock is invalid | Error | Enter a whole number greater than or equal to zero. |
| Product is successfully saved | Success | Product created successfully. Product ID: {product_id}. |
| Employee cancels after entering details | Warning | Unsaved product details will be lost. Cancel creation? (y/n) |

#### Cancellation Behaviour
- If the employee confirms cancellation, discard the entered details.
- Otherwise, return to product entry with the details retained.

#### High-Level Test Scenarios
| ID | Scenario | Expected Result |
|---|---|---|
| CP-01 | Submit valid name, price, and stock | Product saved with all entered details; generated ID displayed. |
| CP-02 | Submit a null, empty, or whitespace-only name | Name-required error; nothing saved. |
| CP-03 | Submit a null, empty, or whitespace-only price | Price-required error; nothing saved. |
| CP-04 | Submit a nonnumeric price | Invalid-price error; nothing saved. |
| CP-05 | Submit zero or a negative price | Invalid-price error; nothing saved. |
| CP-06 | Submit a price with more than two decimal places | Invalid-price error; nothing saved. |
| CP-07 | Submit NaN or infinity as the price | Invalid-price error; nothing saved. |
| CP-08 | Submit valid details with surrounding whitespace | Surrounding whitespace removed; product saved. |
| CP-09 | Create multiple products | Each receives a different, non-null ID. |
| CP-10 | Return to the main menu and view products in the same session | Created product is available. |
| CP-11 | Restart after successful creation | Product collection is empty. |
| CP-12 | Confirm cancellation | Details discarded; nothing saved. |
| CP-13 | Decline cancellation | Entered details retained; entry continues. |
| CP-14 | Submit a quantity of zero with other valid details | Product saved with zero stock. |
| CP-15 | Submit a positive whole-number quantity with other valid details | Product saved with the entered quantity. |
| CP-16 | Submit a null, empty, or whitespace-only quantity | Quantity-required error; nothing saved. |
| CP-17 | Submit a negative, fractional, or nonnumeric quantity | Invalid-quantity error; nothing saved. |

#### Notes
- Use Python's `Decimal` to represent prices.
- Product name uniqueness has not yet been decided.
- Viewing and updating products are covered by separate PBIs.
