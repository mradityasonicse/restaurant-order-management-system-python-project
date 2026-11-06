# Restaurant Order Management System (PS No. 35)
**Bachelor of Technology — Computer Science and Engineering**

A robust, standalone console-based Restaurant Order Management and Billing System developed in **Python 3**. Fully compliant with all 5 Bare Minimum Requirements of Problem Statement No. 35, handling waiter ordering workflows, multi-table orders, input validation, running orders, and tax billing (10% Service Charge & 5% GST).

---

## 📋 Problem Statement Overview

* **PS No.**: 35
* **Project Title**: Restaurant Order Management System
* **Language**: Python 3 (Single `.py` file runnable from console)
* **Core Concepts**: Lists, Dictionaries, Loops, Input Validation, Billing Computations
* **Restaurant Specifications**:
  * **Menu (Dictionary)**: Burger (Rs. 100), Pizza (Rs. 200), Coffee (Rs. 50)
  * **Tables (List per table)**: 20 tables (Numbered 1 to 20)
  * **Service Charge**: 10% on Subtotal
  * **GST**: 5% on Subtotal

---

## 📂 Project Structure

```text
E:\python project resturent order management system\
│
├── restaurant_system.py    # Complete standalone Python 3 console application
├── README.md               # Technical documentation & execution guide
└── summary.md              # Quick verification matrix & test results summary
```

---

## 🎯 Bare Minimum Requirements Compliance

| # | Bare Minimum Requirement | Implementation in `restaurant_system.py` | Status |
|:---:|--------------------------|------------------------------------------|:------:|
| **1** | Write solution in Python 3 (one `.py` file) & run from console | Self-contained in `restaurant_system.py`, runnable directly via CLI | ✅ COMPLIANT |
| **2** | Keep menu in a dictionary & table orders in a list | `MENU = {"Burger": 100, "Pizza": 200, "Coffee": 50}` and `table_orders[t] = []` | ✅ COMPLIANT |
| **3** | Use a loop to take multiple items for a table & show running order | Implemented `while` loop taking items with `format_running_order()` display | ✅ COMPLIANT |
| **4** | Calculate Subtotal, Service charge, GST & Total, print neat bill | `calculate_bill()` computes exact 10% Service Charge + 5% GST and prints neat receipt | ✅ COMPLIANT |
| **5** | Validate table number, item name, and quantity before adding order | `validate_table()`, `validate_item()`, and `validate_quantity()` with graceful error recovery | ✅ COMPLIANT |

---

## 🧪 Test Cases & Expected vs Actual Output

### Test Case 1: Normal Input
* **Input**:
  ```text
  Table: 5
  Order item: Burger
  Quantity: 2
  ```
* **Expected Output**:
  ```text
  Burger x2 added to Table 5 | Amount: 200
  ```
* **Actual Output**:
  ```text
  Burger x2 added to Table 5 | Amount: 200
  ```
* **Status**: **PASS (100% Match — Amount is Rs. 200)**

---

### Test Case 2: Boundary / Minimum Input
* **Input**:
  ```text
  Table: 1
  Order item: Coffee; Quantity: 1
  Generate bill
  ```
* **Expected Output**:
  ```text
  Subtotal: 50 | Service charge (10%): 5.00
  GST (5%): 2.50 | Total: 57.50
  ```
* **Actual Output**:
  ```text
  Subtotal: 50 | Service charge (10%): 5.00
  GST (5%): 2.50 | Total: 57.50
  ```
* **Status**: **PASS (100% Match)**

---

### Test Case 3: Invalid Input Validation
* **(a) Order item: `Pasta`**
  * Expected: `(a) Item not on the menu. Available: Burger, Pizza, Coffee`
  * Actual: `(a) Item not on the menu. Available: Burger, Pizza, Coffee` — **PASS**
* **(b) Quantity: `abc`**
  * Expected: `(b) Invalid quantity. Enter a whole number.`
  * Actual: `(b) Invalid quantity. Enter a whole number.` — **PASS**
* **(c) Table: `0`**
  * Expected: `(c) Invalid table number. Enter a number between 1 and 20.`
  * Actual: `(c) Invalid table number. Enter a number between 1 and 20.` — **PASS**
* **Status**: **PASS (100% Defensive Validation)**

---

### Test Case 4: Different Valid Scenario
* **Input**:
  ```text
  Table: 3
  Order Burger x2, Pizza x1, Coffee x4
  Generate bill
  ```
* **Expected Output**:
  ```text
  Burger x2 = 200 | Pizza x1 = 200 | Coffee x4 = 200
  Subtotal: 600 | Service charge (10%): 60.00
  GST (5%): 30.00 | Total: 690.00
  ```
* **Actual Output**:
  ```text
  Burger x2 = 200 | Pizza x1 = 200 | Coffee x4 = 200
  Subtotal: 600 | Service charge (10%): 60.00
  GST (5%): 30.00 | Total: 690.00
  ```
* **Status**: **PASS (100% Match)**

---

## 🚀 How to Run

### 1. Interactive Console Mode
Open terminal or PowerShell in this directory:
```bash
python restaurant_system.py
```
* Directly enter Table Number (1-20), Order item, and Quantity.
* Type `bill` to generate final bill with taxes.
* Type `test` to run any test case on custom inputs.
* Type `exit` to quit.

### 2. Verify All 4 Test Cases Automatically
```bash
python restaurant_system.py --test all
```

### 3. Verify Individual Test Cases via CLI
```bash
python restaurant_system.py --test 1    # Run Test Case 1
python restaurant_system.py --test 2    # Run Test Case 2
python restaurant_system.py --test 3    # Run Test Case 3
python restaurant_system.py --test 4    # Run Test Case 4
```

---

## 📊 Bill Calculation Formula
$$\text{Subtotal} = \sum (\text{Price} \times \text{Quantity})$$
$$\text{Service Charge (10\%)} = \text{Subtotal} \times 0.10$$
$$\text{GST (5\%)} = \text{Subtotal} \times 0.05$$
$$\text{Total Payable} = \text{Subtotal} + \text{Service Charge} + \text{GST}$$
