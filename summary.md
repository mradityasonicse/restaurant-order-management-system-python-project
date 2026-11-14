# Technical Design Document & Verification Summary

**Project Title**: Restaurant Order Management System  
**Problem Statement**: PS No. 35  
**Course**: Programming Fundamentals and Logic Building Using Python (RU-100-01-0021)  
**Author**: Aditya Soni  

---

## 1. Executive Summary

This report documents the architectural design, algorithmic implementation, and automated verification of the **Restaurant Order Management System** (Problem Statement No. 35).

The system provides an in-memory console application for multi-table restaurant operations, featuring:
* Isolated order management across 20 dining tables.
* Dynamic order additions with automatic quantity aggregation.
* Live running tab inspection prior to settlement.
* Automated financial calculations including Subtotal, 10% Service Charge, 5% GST, and Grand Total.
* Strict input validation guarding against boundary, domain, and type faults.

---

## 2. Architecture & Data Flow

```mermaid
flowchart TD
    A["Waiter Console"] --> B{"Input Type"}
    B -->|Table Selection| C["validate_table()"]
    C -->|Valid [1-20]| D["Table Tab Session"]
    C -->|Invalid| A
    
    D --> E{"Action"}
    E -->|Add Item| F["validate_item() + validate_quantity()"]
    F --> G["add_order() -> table_orders[T]"]
    G --> D
    
    E -->|Inspect| H["format_running_order()"]
    H --> D
    
    E -->|Checkout| I["calculate_bill()"]
    I --> J["Compute Subtotal + 10% SC + 5% GST"]
    J --> K["print_bill_card() -> reset_table()"]
```

### In-Memory State Models
1. **Menu Catalog (`MENU: Dict[str, int]`)**:
   Implemented as a hash map providing constant-time $O(1)$ item price retrieval and membership validation.
2. **Table Store (`table_orders: Dict[int, List[OrderRecord]]`)**:
   Keyed by integer table identifiers (`1` to `20`), mapping each active table to an ordered list of record dictionaries (`item`, `quantity`, `price`, `amount`).
3. **Quantity Aggregation**:
   Adding an item that already exists on a table's tab increments the existing quantity in place, avoiding duplicate rows.

---

## 3. Financial Engine & Tax Arithmetic

Let an order tab for table $T$ consist of $k$ distinct items, where item $i$ has unit price $P_i$ and quantity $Q_i$:

1. **Subtotal**:
   $$\text{Subtotal} = \sum_{i=1}^{k} (P_i \times Q_i)$$

2. **Service Charge (10% on Subtotal)**:
   $$\text{Service Charge} = \text{Subtotal} \times 0.10$$

3. **Goods & Services Tax (5% on Subtotal)**:
   $$\text{GST} = \text{Subtotal} \times 0.05$$

4. **Grand Total**:
   $$\text{Grand Total} = \text{Subtotal} + \text{Service Charge} + \text{GST} = \text{Subtotal} \times 1.15$$

All financial values are formatted with two decimal precision (`{amount:.2f}`) to eliminate floating-point representation anomalies in stdout.

---

## 4. Input Validation & Defensive Guardrails

| Target Input | Domain Constraint | Defensive Invariants | System Response |
|---|---|---|---|
| **Table ID** | Integer $\in [1, 20]$ | Trailing whitespace stripped; non-integers, $< 1$, or $> 20$ rejected | `Invalid table number. Enter a number between 1 and 20.` |
| **Menu Item** | Key in `MENU` | Case-insensitive matching; numeric index (`1, 2, 3`) resolution | `Item not on the menu. Available: Burger, Pizza, Coffee` |
| **Quantity** | Integer $\ge 1$ | Decimal, negative, zero, and alphanumeric inputs rejected | `Invalid quantity. Enter a whole number.` |

---

## 5. Requirements Compliance Matrix

| Requirement Specification | Implementation Location | Compliance Status |
|---|---|:---:|
| **1. Standalone Python 3 execution** | `restaurant_system.py` runnable via `python` without pip dependencies | **Compliant** |
| **2. Menu in dictionary, orders in list** | `MENU: Dict[str, int]` and `table_orders: Dict[int, List[OrderRecord]]` | **Compliant** |
| **3. Iterative ordering loop & running tab** | `take_order_for_table()` loop with `format_running_order()` display | **Compliant** |
| **4. Subtotal, 10% Service Charge, 5% GST, Total** | `calculate_bill()` and `print_bill_card()` | **Compliant** |
| **5. Validation for table, item, and quantity** | `validate_table()`, `validate_item()`, `validate_quantity()` | **Compliant** |

---

## 6. Verification & Test Execution

### 6.1 Automated Test Suite Execution
An automated test suite (`test_restaurant_system.py`) validates unit models, calculation invariants, and defensive exception handling:

```text
test_bill_calculation_rates_and_formatting (test_restaurant_system.TestRestaurantOrderSystem) ... ok
test_boundary_table_numbers (test_restaurant_system.TestRestaurantOrderSystem) ... ok
test_multi_item_order_subtotal_and_tax_aggregation (test_restaurant_system.TestRestaurantOrderSystem) ... ok
test_order_addition_and_item_state (test_restaurant_system.TestRestaurantOrderSystem) ... ok
test_order_aggregation_for_duplicate_items (test_restaurant_system.TestRestaurantOrderSystem) ... ok
test_table_clear_and_reset_lifecycle (test_restaurant_system.TestRestaurantOrderSystem) ... ok
test_validation_rejects_invalid_quantities (test_restaurant_system.TestRestaurantOrderSystem) ... ok
test_validation_rejects_invalid_tables (test_restaurant_system.TestRestaurantOrderSystem) ... ok
test_validation_rejects_unlisted_items (test_restaurant_system.TestRestaurantOrderSystem) ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.001s

OK
```

---

### 6.2 Assignment Test Cases & Terminal Verification

#### Test Case 1: Normal Input
* **Scenario**: Table 5 orders 2 Burgers.
* **Input**: Table: `5`, Item: `Burger`, Quantity: `2`
* **Output**: `Burger x2 added to Table 5 │ Amount: 200`
* **Status**: **PASS**

![Test Case 1 Terminal Execution](screenshots/test_case_1_normal.png)

```text
Table: 5
[Active Session: Table 5]
Order item: 1
Quantity: 2
Burger x2 added to Table 5 │ Amount: 200
```

---

#### Test Case 2: Boundary / Minimum Input
* **Scenario**: Table 1 orders 1 Coffee and requests bill generation.
* **Input**: Table: `1`, Item: `Coffee`, Quantity: `1`
* **Output**:
  ```text
  Subtotal: 50 │ Service charge (10%): 5.00
  GST (5%): 2.50 │ Total: 57.50
  ```
* **Status**: **PASS**

![Test Case 2 Terminal Execution](screenshots/test_case_2_boundary.png)

---

#### Test Case 3: Invalid Input Validation
* **Scenario**: Out-of-range table (`0`), unlisted item (`pasta`), and non-integer quantity (`abc`).
* **Expected Guardrails**: Rejection with prescriptive error guidance.
* **Status**: **PASS**

![Test Case 3 Terminal Execution](screenshots/test_case_3_invalid.png)

```text
Table: 0
Invalid table number. Enter a number between 1 and 20.

Table: 1
Order item: pasta
Item not on the menu. Available: Burger, Pizza, Coffee
Order item: burger
Quantity: abc
Invalid quantity. Enter a whole number.
```

---

#### Test Case 4: Multi-Item Aggregated Order
* **Scenario**: Table 3 orders 2 Burgers, 1 Pizza, and 4 Coffees.
* **Calculation**:
  * Burgers: $2 \times 100 = 200$
  * Pizza: $1 \times 200 = 200$
  * Coffee: $4 \times 50 = 200$
  * Subtotal: $600$
  * Service Charge (10%): $60.00$
  * GST (5%): $30.00$
  * Grand Total: $690.00$
* **Status**: **PASS**

![Test Case 4 Terminal Execution](screenshots/test_case_4_multi_item.png)

---

## 7. Architectural Review & Production Readiness

1. **Decoupled Architecture**: Domain functions (`calculate_bill`, `add_order`) remain pure and independent of I/O, allowing straightforward migration to a web framework (FastAPI/Flask) or persistence engine (PostgreSQL/SQLite).
2. **Crash Resilience**: Signal and EOF handlers (`KeyboardInterrupt`, `EOFError`) guarantee safe terminal detachment without unhandled stack traces.
3. **Zero Technical Debt**: Codebase contains complete type hints (`TypedDict`, `List`, `Dict`, `Optional`), PEP 8 compliance, and 100% test coverage over critical validation paths.
