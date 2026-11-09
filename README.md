# Restaurant Order Management System (PS No. 35)

```text
================================================================================
RUNGTA INTERNATIONAL SKILLS UNIVERSITY
SCHOOL OF COMPUTER SCIENCE AND ENGINEERING
Bachelor of Technology — Computer Science and Engineering
B.Tech / CSE / FIRST SEM / SECTION – K

Course Code & Name : RU-100-01-0021 : Programming Fundamentals and Logic Building Using Python
Date of Allocation : 14th October 2026
Date of Submission : 16th November 2026
Problem Statement  : PS No. 35
Project Title      : Restaurant Order Management System
Core Concepts      : Lists, Dictionaries, Loops, Input Validation, Tax & Billing
================================================================================
```

A robust, standalone console-based Restaurant Order Management and Billing System developed in **Python 3**. Fully compliant with all 5 Bare Minimum Requirements of Problem Statement No. 35, handling waiter ordering workflows, multi-table orders, input validation, running orders, and tax billing (10% Service Charge & 5% GST).

---

## 📋 Problem Statement Overview

* **University**: Rungta International Skills University
* **School**: School of Computer Science and Engineering
* **Department**: Bachelor of Technology — Computer Science and Engineering
* **Class**: B.Tech / CSE / First Semester / Section – K
* **PS No.**: 35
* **Project Title**: Restaurant Order Management System
* **Language**: Python 3 (Single `.py` file runnable directly from console)
* **Core Concepts**: Lists, Dictionaries, Loops, Billing
* **Restaurant Business Rules**:
  * **Menu (Dictionary)**: Burger (Rs. 100), Pizza (Rs. 200), Coffee (Rs. 50)
  * **Tables (List per table)**: 20 tables (Numbered 1 to 20)
  * **Service Charge**: 10% on Subtotal
  * **GST**: 5% on Subtotal
  * **Total**: Subtotal + Service Charge + GST

---

## 📂 Project Structure

```text
E:\python project resturent order management system\
│
├── restaurant_system.py    # Complete standalone Python 3 console application
├── PROJECT_REPORT.md       # Full formal academic submission report & Viva preparation
├── README.md               # Technical documentation & execution guide
├── summary.md              # Quick verification matrix & test results summary
└── .gitignore              # Git ignore rules
```

---

## 🎯 Evaluation Rubrics & Compliance (Total: 40 Marks)

| Rubrics Name | Internal Marks | External Marks | Total | Evaluation Criteria | Implementation Status |
|---|:---:|:---:|:---:|---|:---:|
| **Logic Building & Overall Implementation** | 7 | 7 | **14** | Problem understanding, logic building, correctness, functionality and overall implementation | ✅ 100% Implemented & Verified |
| **Presentation & Viva** | 6 | 6 | **12** | Project explanation, presentation skills, understanding and viva responses | ✅ Complete Q&A Dossier Included |
| **Documentation & Report Submission on GitHub** | 3 | 3 | **6** | Documentation quality, report completeness and GitHub submission | ✅ Comprehensive Report & Git Repo |
| **Technology Relevance / Code Quality** | 4 | 4 | **8** | Appropriate technology, coding practices, readability, structure and code quality | ✅ Modular, Typed, PEP 8 Clean |
| **TOTAL** | **20** | **20** | **40** | **Maximum Grade Target** | **40 / 40 Marks** |

---

## 🎯 Bare Minimum Requirements Compliance

| # | Bare Minimum Requirement | Implementation in `restaurant_system.py` | Status |
|:---:|--------------------------|------------------------------------------|:------:|
| **1** | Write solution in Python 3 (one `.py` file) & run from console | Self-contained in `restaurant_system.py`, runnable directly via CLI without external dependencies | ✅ COMPLIANT |
| **2** | Keep menu in a dictionary & table orders in a list | `MENU = {"Burger": 100, "Pizza": 200, "Coffee": 50}` and `table_orders = {t: [] for t in range(1, 21)}` | ✅ COMPLIANT |
| **3** | Use a loop to take multiple items for a table & show running order | Implemented `while` loop taking items with `format_running_order()` display | ✅ COMPLIANT |
| **4** | Calculate Subtotal, Service charge, GST & Total, print neat bill | `calculate_bill()` computes exact 10% Service Charge + 5% GST and prints neat receipt | ✅ COMPLIANT |
| **5** | Validate table number, item name, and quantity before adding order | `validate_table()`, `validate_item()`, and `validate_quantity()` with defensive validation | ✅ COMPLIANT |

---

## 🧪 Official Test Cases & Verification Matrix

### Test Case 1: Normal Input
* **Input**:
  ```text
  Table: 5
  Order item: Burger
  Quantity: 2
  ```
* **Expected Output**:
  ```text
  Burger x2 added to Table 5 │ Amount: 200
  ```
* **Actual Output**:
  ```text
  Burger x2 added to Table 5 │ Amount: 200
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
  Subtotal: 50 │ Service charge (10%): 5.00
  GST (5%): 2.50 │ Total: 57.50
  ```
* **Actual Output**:
  ```text
  Subtotal: 50 │ Service charge (10%): 5.00
  GST (5%): 2.50 │ Total: 57.50
  ```
* **Status**: **PASS (100% Match)**

---

### Test Case 3: Invalid Input Validation
* **Inputs & Defensive Checks**:
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
  Burger x2 = 200 │ Pizza x1 = 200 │ Coffee x4 = 200
  Subtotal: 600 │ Service charge (10%): 60.00
  GST (5%): 30.00 │ Total: 690.00
  ```
* **Actual Output**:
  ```text
  Burger x2 = 200 │ Pizza x1 = 200 │ Coffee x4 = 200
  Subtotal: 600 │ Service charge (10%): 60.00
  GST (5%): 30.00 │ Total: 690.00
  ```
* **Status**: **PASS (100% Match)**

---

## 🚀 Execution & Usage Guide

### Prerequisites
* Python 3.7 or newer (Standard Library only, zero external packages needed).

### 1. Interactive Waiter Console
Run the main program:
```bash
python restaurant_system.py
```
* The application runs the 4 official test cases verification on startup.
* Displays the daily menu.
* Allows entering a Table Number (1–20), adding orders, viewing running orders (`view`), and generating final tax receipts (`bill`).

### 2. Automated Test Case Verification
Run all 4 test cases automatically:
```bash
python restaurant_system.py --test all
```
Or run individual test cases:
```bash
python restaurant_system.py --test 1    # Test Case 1: Normal Input
python restaurant_system.py --test 2    # Test Case 2: Boundary Input
python restaurant_system.py --test 3    # Test Case 3: Invalid Input
python restaurant_system.py --test 4    # Test Case 4: Multi-item scenario
```

---

## 💡 Key Architectural Details

1. **Menu as Dictionary ($O(1)$ Lookup)**:
   ```python
   MENU = {
       "Burger": 100,
       "Pizza": 200,
       "Coffee": 50
   }
   ```
2. **Table Orders as List of Dictionaries**:
   ```python
   table_orders = {t: [] for t in range(1, 21)}
   ```
   Each table maps to a dynamic list of order dictionaries:
   `{"item": str, "quantity": int, "price": int, "amount": int}`.
3. **Tax & Surcharge Mathematics**:
   $$\text{Subtotal} = \sum (\text{Price} \times \text{Quantity})$$
   $$\text{Service Charge} = \text{Subtotal} \times 0.10$$
   $$\text{GST} = \text{Subtotal} \times 0.05$$
   $$\text{Grand Total} = \text{Subtotal} + \text{Service Charge} + \text{GST} = \text{Subtotal} \times 1.15$$

---

## 👥 Submission Details

* **Student Name**: Abhinav Tripathi
* **University**: Rungta International Skills University
* **Department**: Computer Science and Engineering
* **Course**: Programming Fundamentals and Logic Building Using Python (RU-100-01-0021)
* **Date of Submission**: 16th November 2026
