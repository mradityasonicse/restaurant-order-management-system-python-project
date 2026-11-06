# Project Summary: Restaurant Order Management System
**Bachelor of Technology – Computer Science and Engineering**  
**Problem Statement (PS) No.: 35**  
**Project Title**: Restaurant Order Management System  
**Language**: Python 3 (Single `.py` file)  
**Concepts**: Lists, Dictionaries, Loops, Input Validation, Tax & Billing Computations  

---

## 📌 Executive Summary
The **Restaurant Order Management System** is a standalone, single-file Python application engineered to satisfy all requirements of Problem Statement 35. It handles waiter ordering workflows, multi-table tracking, running order monitoring, and automated tax billing with 10% Service Charge and 5% GST.

---

## ⚙️ Restaurant Business Rules & Formulas

| Component | Rule / Value | Notes |
|---|---|---|
| **Tables** | 20 Tables (Numbered 1 to 20) | Range validated: $1 \le \text{Table} \le 20$ |
| **Menu Items** | Burger: Rs. 100<br>Pizza: Rs. 200<br>Coffee: Rs. 50 | Case-insensitive validation against Dictionary |
| **Quantity** | Positive integers ($\ge 1$) | Validated using `str.isdigit()` and $> 0$ |
| **Service Charge** | 10% on Subtotal | $\text{Service Charge} = \text{Subtotal} \times 0.10$ |
| **GST** | 5% on Subtotal | $\text{GST} = \text{Subtotal} \times 0.05$ |
| **Grand Total** | Subtotal + Service Charge + GST | $\text{Total} = \text{Subtotal} \times 1.15$ |

---

## 📋 Requirements Compliance Matrix

| # | Requirement | Implementation in `restaurant_system.py` | Verification Status |
|:---:|---|---|:---:|
| **1** | Write solution in Python 3 (one `.py` file) and run from console | Self-contained in `restaurant_system.py` | ✅ 100% Passed |
| **2** | Keep menu in a dictionary & table orders in a list | `MENU = {"Burger": 100, ...}`<br>`table_orders = {t: [] for t in range(1, 21)}` | ✅ 100% Passed |
| **3** | Use a loop to take multiple items for a table & show running order | `while` loop taking orders with `format_running_order()` display | ✅ 100% Passed |
| **4** | Calculate Subtotal, Service charge, GST & Total, and print neat bill | `calculate_bill()` and `print_bill_card()` | ✅ 100% Passed |
| **5** | Validate table number, item name, and quantity before adding order | `validate_table()`, `validate_item()`, and `validate_quantity()` | ✅ 100% Passed |

---

## 🧪 Verification & Test Cases Results

All 4 test cases specified in the project problem statement have been executed and verified:

```text
================================================================================
   BACHELOR OF TECHNOLOGY - COMPUTER SCIENCE AND ENGINEERING
   PS No. 35: RESTAURANT ORDER MANAGEMENT SYSTEM - VERIFICATION SUITE
================================================================================
```

### Test Case 1: Normal Input
- **Input**: Table: `5`, Item: `Burger`, Quantity: `2`
- **Expected Output**: `Burger x2 added to Table 5 | Amount: 200`
- **Actual Output**: `Burger x2 added to Table 5 | Amount: 200`
- **Result**: **PASS (100% Match — Amount is Rs. 200)**

### Test Case 2: Boundary / Minimum Input
- **Input**: Table: `1`, Item: `Coffee`, Quantity: `1` $\rightarrow$ Generate bill
- **Expected Output**: `Subtotal: 50 | Service charge (10%): 5.00 | GST (5%): 2.50 | Total: 57.50`
- **Actual Output**: `Subtotal: 50 | Service charge (10%): 5.00 | GST (5%): 2.50 | Total: 57.50`
- **Result**: **PASS (100% Match)**

### Test Case 3: Invalid Input Validation
- **3(a) Item Not on Menu**: Input `Pasta`
  - Expected: `(a) Item not on the menu. Available: Burger, Pizza, Coffee`
  - Actual: `(a) Item not on the menu. Available: Burger, Pizza, Coffee` $\rightarrow$ **PASS**
- **3(b) Invalid Quantity**: Input `abc`
  - Expected: `(b) Invalid quantity. Enter a whole number.`
  - Actual: `(b) Invalid quantity. Enter a whole number.` $\rightarrow$ **PASS**
- **3(c) Invalid Table Number**: Input `0`
  - Expected: `(c) Invalid table number. Enter a number between 1 and 20.`
  - Actual: `(c) Invalid table number. Enter a number between 1 and 20.` $\rightarrow$ **PASS**

### Test Case 4: Different Valid Scenario
- **Input**: Table: `3`, Order `Burger x2`, `Pizza x1`, `Coffee x4` $\rightarrow$ Generate bill
- **Expected Output**:
  - `Burger x2 = 200 | Pizza x1 = 200 | Coffee x4 = 200`
  - `Subtotal: 600 | Service charge (10%): 60.00 | GST (5%): 30.00 | Total: 690.00`
- **Actual Output**:
  - `Burger x2 = 200 | Pizza x1 = 200 | Coffee x4 = 200`
  - `Subtotal: 600 | Service charge (10%): 60.00 | GST (5%): 30.00 | Total: 690.00`
- **Result**: **PASS (100% Match)**

---

## 📁 Repository Structure

| File | Purpose |
|---|---|
| [`restaurant_system.py`](file:///E:/python%20project%20resturent%20order%20management%20system/restaurant_system.py) | Main standalone console script with menu, validation, loops, billing, and test suite |
| [`README.md`](file:///E:/python%20project%20resturent%20order%20management%20system/README.md) | Full technical documentation and execution guide |
| [`summary.md`](file:///E:/python%20project%20resturent%20order%20management%20system/summary.md) | Executive summary, business rules, and verification matrix |
