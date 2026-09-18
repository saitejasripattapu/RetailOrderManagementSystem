### PBI-01: Create a Customer

#### User Story
As a retail employee,
I want to record and save a customer's name and email,
so that the customer can be selected for orders during the current session.

#### Required Fields
- Name
- Email

#### Acceptance Criteria
1. Name and email are mandatory.
2. Remove leading and trailing whitespace before validation and saving.
3. Reject null, empty, or whitespace-only values.
4. Validate the entire email using Python's `re.fullmatch()` with:
   `^[^\s@]+@[^\s@]+\.[^\s@]+$`
5. If validation fails, display the relevant error and allow correction.
   Do not save the customer.
6. The application automatically generates a unique customer ID within the
   current session.
7. Store the customer ID, name, and email together in memory.
8. Display success only after the customer is added to the in-memory collection.
9. Customers remain available during the current session. Restarting the
   application clears all customers.

#### In-Memory Storage Requirements
| Field | Constraint |
|---|---|
| customer_id | Automatically generated, non-null, and unique within the session |
| name | Required; cannot be null or blank |
| email | Required; cannot be null or blank |

The application validates customer details before adding them to the collection.

#### Messages
| Situation | Type | Message |
|---|---|---|
| Name is missing or blank | Error | Customer name is required. |
| Email is missing or blank | Error | Customer email is required. |
| Email format is invalid | Error | Enter a valid email address, such as name@example.com. |
| Customer is successfully saved | Success | Customer created successfully. Customer ID: {customer_id}. |
| Employee cancels after entering details | Warning | Unsaved customer details will be lost. Cancel creation? (y/n) |

#### Cancellation Behaviour
- If the employee confirms cancellation, discard the entered details.
- Otherwise, return to customer entry with the details retained.

#### High-Level Test Scenarios
| ID | Scenario | Expected Result |
|---|---|---|
| CC-01 | Submit valid name and email | Customer saved; generated ID displayed. |
| CC-02 | Submit a null, empty, or whitespace-only name | Name-required error; nothing saved. |
| CC-03 | Submit a null, empty, or whitespace-only email | Email-required error; nothing saved. |
| CC-04 | Submit an incorrectly formatted email | Email-format error; nothing saved. |
| CC-05 | Submit valid details with surrounding whitespace | Surrounding whitespace removed; customer saved. |
| CC-06 | Create multiple customers | Each receives a different, non-null ID. |
| CC-07 | Return to the main menu and view customers in the same session | Created customer is available. |
| CC-08 | Restart after successful creation | Customer collection is empty. |
| CC-09 | Confirm cancellation | Details discarded; nothing saved. |
| CC-10 | Decline cancellation | Entered details retained; entry continues. |

#### Notes
- Email validation checks format, not whether the address exists.
- Email uniqueness has not yet been decided.
- Customer type selection is covered by a separate PBI.
