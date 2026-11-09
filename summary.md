# Project Summary: Restaurant Order Management System

## Overview
* **Project Name**: Restaurant Order Management System
* **Course**: Programming Fundamentals and Logic Building Using Python (RU-100-01-0021)
* **Class**: B.Tech CSE (First Semester, Section K)
* **Problem Statement**: PS No. 35
* **Implementation Language**: Python 3 (Single standalone script, standard library only)

This project implements a console-based ordering and billing workflow for a restaurant with 20 tables. It covers menu management, multi-table order tracking, live running totals, defensive input validation, and tax calculation (10% Service Charge and 5% GST).

---

## Requirements Checklist

| # | Requirement | Implementation | Status |
|---|---|---|---|
| 1 | Python 3 single `.py` file run from console | Self-contained in `restaurant_system.py` | Complete |
| 2 | Menu in a dictionary & table orders in a list | `MENU` dictionary and `table_orders[table_num]` list | Complete |
| 3 | Loop to take multiple items and show running order | Interactive `while` loop with `format_running_order()` | Complete |
| 4 | Compute subtotal, service charge, GST & print bill | `calculate_bill()` and formatted bill card | Complete |
| 5 | Validate table, item name, and quantity | `validate_table()`, `validate_item()`, `validate_quantity()` | Complete |

---

## Core Data Structures & Design

1. **Menu (`MENU`)**:
   - Type: `dict`
   - Mapping: `{"Burger": 100, "Pizza": 200, "Coffee": 50}`
   - Why: Direct $O(1)$ lookup for prices and easy iteration when showing available items.

2. **Table Storage (`table_orders`)**:
   - Type: `dict` mapping table number (`1..20`) to `list` of orders.
   - Initialized as: `{1: [], 2: [], ..., 20: []}`
   - Why: Keeps tables independent. Adding an order to Table 3 does not touch Table 5.

3. **Order Item Format**:
   - Stored as small dictionaries appended to the table's list:
     ```python
     {
         "item": "Burger",
         "quantity": 2,
         "price": 100,
         "amount": 200
     }
     ```

---

## Billing Calculations

* **Subtotal**: $\sum (\text{Price} \times \text{Quantity})$
* **Service Charge (10%)**: $\text{Subtotal} \times 0.10$
* **GST (5%)**: $\text{Subtotal} \times 0.05$
* **Total Payable**: $\text{Subtotal} + \text{Service Charge} + \text{GST} = \text{Subtotal} \times 1.15$

Amounts are formatted to 2 decimal places to ensure clear currency presentation without rounding artifacts.

---

## Key Functions in `restaurant_system.py`

* `validate_table(val)`: Confirms table is an integer between 1 and 20.
* `validate_item(val)`: Normalizes casing and validates against `MENU` keys.
* `validate_quantity(val)`: Ensures positive integer ($\ge 1$).
* `add_order(table_num, item, qty)`: Computes item amount and appends to table's order list.
* `get_running_order(table_num)`: Returns active orders for the selected table.
* `calculate_bill(table_num)`: Calculates subtotal, taxes, and final total.
* `reset_table(table_num)`: Clears order list after bill payment.
* `run_all_tests_auto()`: Executes all 4 official test cases and displays pass/fail results.

---

## Test Verification Summary

* **Test Case 1 (Normal Input)**: Table 5, Burger x2 -> Amount: 200 (**PASS**)
* **Test Case 2 (Boundary Input)**: Table 1, Coffee x1 -> Subtotal: 50, Service Charge: 5.00, GST: 2.50, Total: 57.50 (**PASS**)
* **Test Case 3 (Invalid Inputs)**: Rejects pasta (not on menu), non-integer quantity, and table 0 (**PASS**)
* **Test Case 4 (Multi-item)**: Table 3, Burger x2, Pizza x1, Coffee x4 -> Subtotal: 600, Total: 690.00 (**PASS**)

---

## Quick Viva Preparation Notes

* **Q: Why use a dictionary for the menu instead of a list?**
  * *A*: A dictionary gives $O(1)$ key-based price lookup, whereas searching a list of pairs takes $O(n)$ time.
* **Q: Why store table orders in a list?**
  * *A*: The problem specifically required a list per table. It preserves order history sequentially and makes it easy to iterate when printing the bill or computing running totals.
* **Q: How are tables cleared after payment?**
  * *A*: When the bill is paid, `reset_table(table_num)` sets `table_orders[table_num] = []`, freeing the table for new customers.
* **Q: How does the program prevent crashes from bad user inputs?**
  * *A*: Input validation functions use `try-except` blocks and regex/checks to catch non-digit numbers, invalid tables, and unknown items before anything is added to the data structures.
