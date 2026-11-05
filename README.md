# Restaurant Order Management System (PS No. 35)
**Bachelor of Technology — Computer Science and Engineering**

A robust, console-based Restaurant Order Management and Billing System developed in **Python 3**. Designed specifically to meet all requirements of Problem Statement 35, handling waiter workflows, multi-table orders, input validation, running orders, and tax billing (Service Charge & GST).

---

## 📋 Problem Statement Overview

* **PS No.**: 35
* **Project Title**: Restaurant Order Management System
* **Language**: Python 3
* **Core Concepts**: Lists, Dictionaries, Loops, Input Validation, Tax & Billing Computations
* **Restaurant Specifications**:
  * **Menu**: Burger (Rs. 100), Pizza (Rs. 200), Coffee (Rs. 50)
  * **Tables**: 20 tables (Numbered 1 to 20)
  * **Service Charge**: 10% on Subtotal
  * **GST**: 5% on Subtotal

---

## 📂 Project Directory Structure

```text
E:\python project resturent order management system\
│
├── restaurant_system.py          # Core console application (Single .py file)
├── app.py                        # Web POS Frontend Dashboard (Flask UI)
├── test_cases_runner.py          # Automated verification suite (All 4 test cases)
├── generate_screenshots.py       # High-definition terminal screenshot generator
├── run_website.bat               # 1-Click launcher for Web POS Dashboard
├── run_console.bat               # 1-Click launcher for Waiter Console
├── run_tests.bat                 # 1-Click launcher for Test Runner
├── README.md                     # Project documentation & execution guide
├── summary.md                    # Quick executive summary & verification table
├── PROJECT_REPORT.md             # Formal college submission report
├── .vscode/                      # VS Code launch & settings configurations
└── screenshots\                  # Captured visual proof of passing test cases
    ├── testcase_1_normal_input.png
    ├── testcase_2_boundary_min_input.png
    ├── testcase_3_invalid_input.png
    ├── testcase_4_different_valid_scenario.png
    └── all_test_cases_summary.png
```

---

## 🎯 Bare Minimum Requirements Compliance

| # | Bare Minimum Requirement | Implementation Details in `restaurant_system.py` | Status |
|---|--------------------------|---------------------------------------------------|:------:|
| 1 | Write solution in Python 3 (one `.py` file) & run from console | Self-contained in `restaurant_system.py`, runnable directly via CLI | ✅ COMPLIANT |
| 2 | Keep menu in a dictionary & table orders in a list | `MENU = {"Burger": 100, ...}` and `table_orders[t] = []` | ✅ COMPLIANT |
| 3 | Use a loop to take multiple items for a table & show running order | Implemented `while` loop taking items with `format_running_order()` display | ✅ COMPLIANT |
| 4 | Calculate Subtotal, Service charge, GST & Total, print neat bill | `calculate_bill()` computes exact 10% Service Charge + 5% GST and prints bill | ✅ COMPLIANT |
| 5 | Validate table number, item name, and quantity before adding order | `validate_table()`, `validate_item()`, and `validate_quantity()` | ✅ COMPLIANT |

---

## 🧪 Test Cases & Expected vs Actual Output

### Test Case 1: Normal Input
* **Input**: Table: `5`, Item: `Burger`, Quantity: `2`
* **Expected Output**: `Burger x2 added to Table 5 | Amount: 200`
* **Actual Output**: `Burger x2 added to Table 5 | Amount: 200`
* **Status**: **PASS (100% Match)**

### Test Case 2: Boundary / Minimum Input
* **Input**: Table: `1`, Item: `Coffee`, Quantity: `1` → Generate Bill
* **Expected Output**: `Subtotal: 50 | Service charge (10%): 5.00 | GST (5%): 2.50 | Total: 57.50`
* **Actual Output**: `Subtotal: 50 | Service charge (10%): 5.00 | GST (5%): 2.50 | Total: 57.50`
* **Status**: **PASS (100% Match)**

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

### Test Case 4: Different Valid Scenario
* **Input**: Table: `3`, Order: `Burger x2`, `Pizza x1`, `Coffee x4` → Generate Bill
* **Expected Output**:
  * `Burger x2 = 200 | Pizza x1 = 200 | Coffee x4 = 200`
  * `Subtotal: 600 | Service charge (10%): 60.00 | GST (5%): 30.00 | Total: 690.00`
* **Actual Output**:
  * `Burger x2 = 200 | Pizza x1 = 200 | Coffee x4 = 200`
  * `Subtotal: 600 | Service charge (10%): 60.00 | GST (5%): 30.00 | Total: 690.00`
* **Status**: **PASS (100% Match)**

---

## 🚀 How to Run

### 1. Interactive Console Mode
Open terminal or PowerShell in this directory:
```bash
python restaurant_system.py
```

### 2. Run Automated Verification Test Suite (All 4 Test Cases)
```bash
python test_cases_runner.py
# or directly:
python restaurant_system.py --test
```

### 3. Launch Web POS Frontend Dashboard (Browser UI)
```bash
python app.py
```
Open **`http://127.0.0.1:5000`** in your browser to access the full visual POS system, visual table selector (1-20), menu cards, and test execution buttons.

### 4. Regenerate Visual Screenshots
```bash
python generate_screenshots.py
```
Screenshots will be saved in the `screenshots/` directory.

### 5. Running in VS Code
1. Open this folder in VS Code: `code "E:\python project resturent order management system"`
2. Press **`F5`** or go to the **Run & Debug (Ctrl+Shift+D)** panel to choose:
   - `Python: Interactive Restaurant Console (restaurant_system.py)`
   - `Python: Run All 4 Test Cases (test_cases_runner.py)`
   - `Python: Launch Web Frontend Dashboard (app.py)`

---

## 🛠️ Errors & Defensive Exception Handling Architecture

1. **Table Out of Range or String Input**:
   * *Problem*: Users might enter `0`, `25`, or non-numeric characters like `"table five"`.
   * *Handled By*: `validate_table()` uses `int()` wrapped in `try...except ValueError` and checks `1 <= table <= 20`.
2. **Item Not in Menu**:
   * *Problem*: If waiter inputs `"Pasta"` or typos like `"Burgerr"`, standard dictionary lookups crash with a `KeyError`.
   * *Handled By*: `validate_item()` checks case-insensitively against `MENU.keys()`, raising a user-friendly error with available options.
3. **Invalid Quantity**:
   * *Problem*: Waiter enters `"abc"`, negative numbers (`-2`), or floats (`2.5`).
   * *Handled By*: `validate_quantity()` strictly checks `str.isdigit()` and `int(qty) > 0`, ensuring only valid positive whole numbers are accepted.
