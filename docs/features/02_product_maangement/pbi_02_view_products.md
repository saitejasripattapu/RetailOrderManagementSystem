### PBI-02: View Products

#### User Story
As a retail employee,
I want to view products, their prices, and stock,
so that I can identify products when creating an order.

#### Acceptance Criteria
1. Retrieve products from the current session's in-memory collection.
2. Display each product's ID, name, price, and stock.
3. Display products in ascending order of product ID.
4. Display prices with two decimal places.
5. If no products exist, display:
   "No products found. Create a product first."
6. Viewing products must not change their saved details.
7. Allow the employee to return to the main menu.
8. Include products with zero stock and display their quantity as 0.

#### Messages
| Situation | Type | Message |
|---|---|---|
| No products exist | Information | No products found. Create a product first. |

#### High-Level Test Scenarios
| ID | Scenario | Expected Result |
|---|---|---|
| VP-01 | View a single saved product | Correct ID, name, price, and stock are displayed. |
| VP-02 | View multiple products | All products appear in ascending product ID order. |
| VP-03 | View products with identical names | Separate records are displayed with distinct IDs. |
| VP-04 | View a product with a price of 5 or 5.5 | Price is displayed as 5.00 or 5.50, respectively. |
| VP-05 | View when no products exist | "No products found" message appears. |
| VP-06 | Restart the application and view products | "No products found" message appears. |
| VP-07 | Return to the main menu | Main menu is displayed. |
| VP-08 | Check records after viewing | Saved product details remain unchanged. |
| VP-09 | View a product with available stock | Correct stock is displayed. |
| VP-10 | View a product with zero stock | Product is displayed with stock of 0. |

#### Dependencies
- PBI-01: Create a Product.

#### Scope
- Searching, filtering, and editing products are not included.
- Products with zero stock are displayed.
- Stock changes when processing orders are covered by Order Management.
