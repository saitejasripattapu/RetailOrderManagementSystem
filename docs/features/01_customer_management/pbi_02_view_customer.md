### PBI-02: View Customers

#### User Story
As a retail employee,
I want to view saved customers,
so that I can identify a customer when creating an order.

#### Acceptance Criteria
1. Retrieve customers from the current session's in-memory collection.
2. Display each customer's ID, name, email, and customer type.
3. Display customers in ascending order of customer ID.
4. If no customers exist, display:
   "No customers found. Create a customer first."
5. Viewing customers must not change their saved details.
6. Allow the employee to return to the main menu.

#### Messages
| Situation | Type | Message |
|---|---|---|
| No customers exist | Information | No customers found. Create a customer first. |

#### High-Level Test Scenarios
| ID | Scenario | Expected Result |
|---|---|---|
| VC-01 | View a single saved customer | Correct ID, name, email, and type are displayed. |
| VC-02 | View multiple customers | All customers appear in ascending customer ID order. |
| VC-03 | View customers with identical names | Separate records are displayed with distinct IDs. |
| VC-04 | View when no customers exist | "No customers found" message appears. |
| VC-05 | Restart the application and view customers | "No customers found" message appears. |
| VC-06 | Return to the main menu | Main menu is displayed. |
| VC-07 | Check records after viewing | Saved customer details remain unchanged. |

#### Dependencies
- PBI-01: Create a Customer.
- PBI-03: Assign a Customer Type supplies the displayed customer type.

#### Scope
- Searching, filtering, and editing customers are not included.
