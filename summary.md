# Project Summary: Restaurant Order Management System
**Bachelor of Technology – Computer Science and Engineering**  
**Problem Statement (PS) No.: 35**  
**Project Title**: Restaurant Order Management System  
**Language**: Python 3  
**Concepts**: Lists, Dictionaries, Loops, Input Validation, Tax & Billing Computations  

---

## 📌 Executive Summary
The **Restaurant Order Management System** is a software solution engineered to streamline waiter ordering operations, table tracking, running order monitoring, and automated tax billing in a multi-table dining restaurant.

The system features **dual-interface execution**:
1. **Core Single-File Console Application (`restaurant_system.py`)**: Fulfills 100% of the academic bare minimum requirements.
2. **Interactive Web POS Dashboard (`app.py`)**: A modern browser-based point-of-sale interface running locally at `http://127.0.0.1:5000` with visual tables, menu cards, and one-click test verification.

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

| # | Requirement | Implementation in Code | Verification Status |
|:---:|---|---|:---:|
| **1** | Write solution in Python 3 (one `.py` file) and run from console | Self-contained in `restaurant_system.py` | ✅ 100% Passed |
| **2** | Keep menu in a dictionary & table orders in a list | `MENU = {"Burger": 100, ...}`<br>`table_orders = {t: [] for t in range(1, 21)}` | ✅ 100% Passed |
| **3** | Use a loop to take multiple items for a table & show running order | `while` loop taking orders with `format_running_order()` display | ✅ 100% Passed |
| **4** | Calculate Subtotal, Service charge, GST & Total, and print neat bill | `calculate_bill()` and `print_bill_card()` | ✅ 100% Passed |
| **5** | Validate table number, item name, and quantity before adding order | `validate_table()`, `validate_item()`, and `validate_quantity()` | ✅ 100% Passed |

---

## 🧪 Verification & Test Cases Results

All 4 test cases specified in the project problem statement have been executed and verified:

```
================================================================================
   BACHELOR OF TECHNOLOGY - COMPUTER SCIENCE AND ENGINEERING
   PS No. 35: RESTAURANT ORDER MANAGEMENT SYSTEM - VERIFICATION SUITE
================================================================================
```

### Test Case 1: Normal Input
- **Input**: Table: `5`, Item: `Burger`, Quantity: `2`
- **Expected Output**: `Burger x2 added to Table 5 | Amount: 200`
- **Actual Output**: `Burger x2 added to Table 5 | Amount: 200`
- **Result**: **PASS (100% Match)**

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

## 📁 Project Files & Artifacts

| File / Folder | Purpose |
|---|---|
| [`restaurant_system.py`](file:///E:/python%20project%20resturent%20order%20management%20system/restaurant_system.py) | Main standalone console script with menu, validation, and billing |
| [`app.py`](file:///E:/python%20project%20resturent%20order%20management%20system/app.py) | Modern Flask Web POS dashboard with auto-opening browser |
| [`test_cases_runner.py`](file:///E:/python%20project%20resturent%20order%20management%20system/test_cases_runner.py) | Standalone automated verification runner for all 4 test cases |
| [`generate_screenshots.py`](file:///E:/python%20project%20resturent%20order%20management%20system/generate_screenshots.py) | Script to generate pixel-perfect PNG terminal proofs |
| [`README.md`](file:///E:/python%20project%20resturent%20order%20management%20system/README.md) | Full technical documentation and operational guide |
| [`PROJECT_REPORT.md`](file:///E:/python%20project%20resturent%20order%20management%20system/PROJECT_REPORT.md) | Academic college report with flowcharts and complexity analysis |
| [`run_website.bat`](file:///E:/python%20project%20resturent%20order%20management%20system/run_website.bat) | 1-Click double-clickable batch launcher for Web POS Dashboard |
| [`run_console.bat`](file:///E:/python%20project%20resturent%20order%20management%20system/run_console.bat) | 1-Click double-clickable batch launcher for Waiter Console |
| [`run_tests.bat`](file:///E:/python%20project%20resturent%20order%20management%20system/run_tests.bat) | 1-Click double-clickable batch launcher for Verification Suite |
| [`screenshots/`](file:///E:/python%20project%20resturent%20order%20management%20system/screenshots) | High-definition PNG images of all 4 test case runs |

---

## 🚀 How to Run Quick Reference

1. **Launch Web POS Website:**
   - Double-click `run_website.bat` OR run:
     ```bash
     python app.py
     ```
   - Open browser at: **`http://127.0.0.1:5000`**

2. **Launch Waiter Console:**
   - Double-click `run_console.bat` OR run:
     ```bash
     python restaurant_system.py
     ```

3. **Run Automated Test Cases:**
   - Double-click `run_tests.bat` OR run:
     ```bash
     python test_cases_runner.py
     ```
