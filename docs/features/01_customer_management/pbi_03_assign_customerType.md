### PBI-03: Assign a Customer Type

#### User Story
As a retail employee,
I want to assign a type when creating a customer,
so that their orders use the appropriate pricing and discount rules.

#### Acceptance Criteria
1. Display the available customer types:
   - Regular
   - Premium
   - Corporate
2. Assign Regular if the employee leaves the selection blank.
3. Accept type names regardless of letter case and remove surrounding
   whitespace.
4. Save the type using its standard name: Regular, Premium, or Corporate.
5. Reject unsupported types, display an error, and allow correction.
6. Do not save the customer until the type and other required details
   are valid.
7. Store the selected type with the customer in memory.
8. Display the saved type when viewing customers.
9. Retain the saved type for the current session. Customer records are cleared
   when the application restarts.

#### Business Rules
- Regular is the default customer type.
- The employee determines eligibility before selecting a type.
- The application does not verify membership or business eligibility.
- Discount calculation is covered by the Pricing and Discounts feature:
  - Regular: 2%
  - Premium: 5%
  - Corporate: 7%

#### Application Validation Requirements
- Customer type cannot be null.
- Only Regular, Premium, and Corporate are allowed.
- The application assigns Regular when the selection is blank.

#### Messages
| Situation | Type | Message |
|---|---|---|
| Selection is blank | Information | No customer type selected. Regular will be assigned. |
| Type is unsupported | Error | Invalid customer type. Choose Regular, Premium, or Corporate. |

Successful saving uses the message defined in PBI-01.
No additional warning is required for type selection.

#### High-Level Test Scenarios
| ID | Scenario | Expected Result |
|---|---|---|
| CT-01 | Select Regular | Customer is saved as Regular. |
| CT-02 | Select Premium | Customer is saved as Premium. |
| CT-03 | Select Corporate | Customer is saved as Corporate. |
| CT-04 | Leave selection blank or enter only spaces | Regular is assigned; default message appears. |
| CT-05 | Enter `premium` or `PREMIUM` | Accepted and saved as Premium. |
| CT-06 | Enter ` Corporate ` | Surrounding spaces removed; saved as Corporate. |
| CT-07 | Enter an unsupported type | Error displayed; customer not saved; correction allowed. |
| CT-08 | Correct an invalid type to a supported type | Customer saves when all other details are valid. |
| CT-09 | Return to the main menu and view the customer in the same session | Previously saved customer type is displayed. |

#### Dependencies
- PBI-01: Create a Customer integrates type selection before saving.
- PBI-02: View Customers displays the saved type.

#### Scope
Changing the type of an existing customer is outside this PBI.
