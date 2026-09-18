# Solution Design

## Encapsulation and controlled state changes

Important business data will be stored in internal attributes and exposed through
read-only properties. Changes will go through methods that enforce the business
rules. Constructor validation alone is insufficient: later changes must also
preserve validity.

| Data | Business rule | Design decision |
|---|---|---|
| Product ID | Generated within the session; unique and unchanged after creation | Expose a read-only property; the application assigns IDs and checks collection membership. |
| Product name | Required and not blank after trimming | Store internally; change through `Product.update()` after validation. |
| Product price | Finite `Decimal`, greater than zero, at most two decimal places | Store as `_price`; expose a read-only `price` property. Validate proposed updates before assignment. |
| Product stock | Whole number greater than or equal to zero | Store as `_stock`; expose a read-only `stock` property. Product updates replace stock after validation; order additions use controlled stock reduction. |
| Order item quantity | Positive whole number; a new addition cannot exceed current product stock | Validate when adding an item. Keep the stored quantity read-only, since editing items is outside the current scope. |
| Captured item name and unit price | Preserve the values at the time of addition | Copy into the order item and expose read-only values. Subsequent product updates must not change them. |
| Order items | Every item must be valid and belong to its order | Keep the collection internal; expose a tuple for viewing and add items through a controlled operation. Item fields must also be protected. |
| Customer ID, name, and email | Validated during creation; editing customers is outside the current scope | Expose read-only properties after construction. Check case-insensitive email uniqueness in the application that manages customers. |
| Customer type | Regular, Premium, or Corporate | Select the corresponding subclass during creation; expose its type without a public setter. Changing type is outside the current scope. |

## Failure behavior

- Invalid values passed to constructors or update methods raise `ValueError`
  with an understandable message. The CLI catches this and allows correction.
- Direct assignment to a read-only property raises `AttributeError`. Callers
  must use the supported methods instead.
- Validate every proposed product update before changing any stored field.
  If one value is invalid, retain all previous values.
- Check stock again inside the operation that reduces it; a separate availability
  check alone must not authorize an unchecked reduction.
- Coordinate order item addition and stock reduction so both succeed or neither
  changes. Prepare and validate the item before committing changes; roll back
  if a subsequent commit step fails.
- Calculate subtotals, discounts, and final amounts from stored items rather
  than exposing freely assignable totals.

## Python access conventions

A leading underscore indicates internal use, not strict privacy. Read-only
properties block accidental assignment through the public interface, while
validated methods provide the supported path for changes. This is a design
boundary for cooperating code, not a security barrier.

## Current implementation and remaining work

The current `Product` constructor and `update()` validate name, price, and stock;
`update()` validates all fields before assignment. Product ID already has a
read-only property. However, product name, price, and stock are still public
attributes, so direct assignment can bypass validation.

Customer creation validates name and email, but its attributes remain publicly
assignable. Order and OrderItem are not implemented yet. The protections above
are design decisions to implement; they are not all present in the current code.
