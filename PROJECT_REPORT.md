# ACADEMIC PROJECT REPORT
## PS No. 35: Restaurant Order Management System
**Course:** Bachelor of Technology in Computer Science and Engineering  
**Language:** Python 3  
**Status:** 100% Implemented & Verified with 4/4 Test Cases  

---

## 1. Introduction & Problem Definition

In modern hospitality services, point-of-sale and table ordering systems must maintain high transactional accuracy, real-time running tab tracking, and dependable billing. 

The objective of **Problem Statement 35** is to engineer a console-based **Restaurant Order Management System** in Python 3 that allows a waiter to:
1. Select any designated dining table (Tables 1 to 20).
2. Take food and beverage orders from a predefined menu (Burger Rs.100, Pizza Rs.200, Coffee Rs.50).
3. Display the running order dynamically as items are added.
4. Calculate the financial bill including:
   * **Subtotal** (Gross total of all items ordered).
   * **Service Charge** (10% on the subtotal).
   * **GST** (5% on the subtotal).
   * **Grand Total** (Subtotal + Service Charge + GST).
5. Strictly validate all user inputs (table number, item names, and quantities) to prevent runtime crashes.

---

## 2. Core Python Concepts Used

| Concept | Implementation in Project | Purpose / Academic Justification |
| :--- | :--- | :--- |
| **Dictionaries (`dict`)** | `MENU = {"Burger": 100, "Pizza": 200, "Coffee": 50}` | Provides $O(1)$ constant time lookup for item pricing and name validation. |
| **Lists (`list`)** | `table_orders = {t: [] for t in range(1, 21)}` | Each table maintains a dynamic list of orders where multiple items can be sequentially appended. |
| **Loops (`while`, `for`)** | `while True` waiter loop, `for` order accumulation | Allows continuous order entry until the waiter finishes, and iterates over orders to compute totals. |
| **Exception Handling (`try-except`)** | `try: int(qty) except ValueError:` | Prevents terminal crashes from invalid user inputs such as `"abc"` or symbols. |
| **Arithmetic & Float Formatting** | `subtotal * 0.10`, `subtotal * 0.05`, `f"{val:.2f}"` | Enforces exact 2-decimal financial precision for GST and Service charge. |

---

## 3. Data Structures & Architectural Design

### 3.1 Data Flow
```
[ Waiter Console ]
        │
        ▼
[ Input Layer ] (Table, Item, Quantity)
        │
        ▼
[ Validation Guard Layer ]
 ├─ validate_table()    -> Checks range [1, 20] & integer type
 ├─ validate_item()     -> Case-insensitive lookup against MENU
 └─ validate_quantity() -> Validates positive whole integers
        │
        ▼
[ Order State Engine ]
 └─ table_orders[table_num].append({item, quantity, price, amount})
        │
        ▼
[ Billing & Output Engine ]
 ├─ format_running_order()
 └─ calculate_bill() -> Subtotal + 10% Service Charge + 5% GST = Total
```

---

## 4. Error Analysis & Defensive Programming

During development, common edge-cases and errors were identified and resolved:

### 4.1 `ValueError` on Non-Numeric Inputs
* **Vulnerability**: If waiter types `"abc"` or `""` when asked for quantity or table number, Python's default `int()` throws `ValueError` and terminates the program.
* **Solution**: Custom validation functions `validate_table()` and `validate_quantity()` wrap parsing inside `try...except ValueError` blocks and verify boundary conditions, returning explicit user feedback without program termination.

### 4.2 `KeyError` on Non-Existent Menu Items
* **Vulnerability**: If an item such as `"Pasta"` is requested, direct dictionary access `MENU[item]` raises `KeyError`.
* **Solution**: `validate_item()` scans keys case-insensitively and returns `Item not on the menu. Available: Burger, Pizza, Coffee`.

### 4.3 Boundary Violations on Table Numbers
* **Vulnerability**: Tables in the restaurant are strictly numbered 1 to 20. Inputs such as `0`, `-1`, or `21` must be rejected.
* **Solution**: Verified condition `1 <= table_number <= 20`.

---

## 5. Test Execution Matrix (All 4 Required Test Cases)

| Test Case | Scenario / Category | Inputs Provided | Expected Output | Actual Output | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **1** | **Normal Input** | Table: `5`<br>Item: `Burger`<br>Qty: `2` | `Burger x2 added to Table 5 \| Amount: 200` | `Burger x2 added to Table 5 \| Amount: 200` | **PASS** ✅ |
| **2** | **Boundary / Min Input** | Table: `1`<br>Item: `Coffee`<br>Qty: `1`<br>Action: Bill | `Subtotal: 50 \| Service charge (10%): 5.00 \| GST (5%): 2.50 \| Total: 57.50` | `Subtotal: 50 \| Service charge (10%): 5.00 \| GST (5%): 2.50 \| Total: 57.50` | **PASS** ✅ |
| **3(a)**| **Invalid Item** | Item: `Pasta` | `(a) Item not on the menu. Available: Burger, Pizza, Coffee` | `(a) Item not on the menu. Available: Burger, Pizza, Coffee` | **PASS** ✅ |
| **3(b)**| **Invalid Quantity** | Qty: `abc` | `(b) Invalid quantity. Enter a whole number.` | `(b) Invalid quantity. Enter a whole number.` | **PASS** ✅ |
| **3(c)**| **Invalid Table** | Table: `0` | `(c) Invalid table number. Enter a number between 1 and 20.` | `(c) Invalid table number. Enter a number between 1 and 20.` | **PASS** ✅ |
| **4** | **Multi-Item Scenario** | Table: `3`<br>Orders: `Burger x2, Pizza x1, Coffee x4`<br>Action: Bill | Line 1: `Burger x2 = 200 \| Pizza x1 = 200 \| Coffee x4 = 200`<br>Line 2: `Subtotal: 600 \| Service charge (10%): 60.00 \| GST (5%): 30.00 \| Total: 690.00` | Line 1: `Burger x2 = 200 \| Pizza x1 = 200 \| Coffee x4 = 200`<br>Line 2: `Subtotal: 600 \| Service charge (10%): 60.00 \| GST (5%): 30.00 \| Total: 690.00` | **PASS** ✅ |

---

## 6. Verification Artifacts & Visual Proof

Screenshots of every passing test case and the master test runner execution are generated and stored in:
`E:\python project resturent order management system\screenshots\`

* `testcase_1_normal_input.png`
* `testcase_2_boundary_min_input.png`
* `testcase_3_invalid_input.png`
* `testcase_4_different_valid_scenario.png`
* `all_test_cases_summary.png`

---

## 7. Conclusion

The application completely fulfills all **Bare Minimum Requirements** and **Instructions** specified in Problem Statement 35:
1. Developed as a clean, single `.py` file (`restaurant_system.py`).
2. Implemented with native Python dictionaries for menu pricing and lists for table orders.
3. Incorporates a dynamic looping structure for multi-item table orders.
4. Calculates subtotal, 10% service charge, 5% GST, and prints structured bills.
5. Employs comprehensive validation preventing crashes and handling all specified error conditions.
