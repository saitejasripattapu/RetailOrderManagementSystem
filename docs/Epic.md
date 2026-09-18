# Epic: Manage Retail Customers, Products, and Orders

## Description
As a retail employee, I want a command-line application to manage
customers, products, and orders, so that order amounts are calculated
using the appropriate pricing or discount rules for each customer type.

## Features

### 1. Customer Management
- Create customers.
- Support Regular, Premium, and Corporate customer types.
- View customers for selection when creating orders.

### 2. Product Management
- Add products.
- View available products and prices.
- Update product details and prices.

### 3. Order Management
- Create an order for a customer.
- Add products with quantities to an order.
- View an order and its items.

### 4. Pricing and Discounts
- Calculate the order subtotal.
- Apply pricing or discount rules based on customer type.
- Display the final order amount.

## Technical Requirements
- Use Python.
- Provide a command-line interface.
- Model the business using Object-Oriented Programming.
- Store customers, products, and orders in memory during the current session.
- Start with empty collections each time the application runs. Data is lost
  when the application closes; database and file persistence are out of scope
  for now.

## Business Rules to Define
- Pricing or discount behaviour for Regular customers.
- Pricing or discount behaviour for Premium customers.
- Pricing or discount behaviour for Corporate customers.
