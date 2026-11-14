# Restaurant Order Management System

A production-grade, zero-dependency console application in Python 3 for restaurant table order dispatch, state management, and automated tax billing.

---

## Architecture & System Design

The system is designed with a strict separation between domain state, financial calculations, input validation pipelines, and terminal presentation:

```
┌────────────────────────────────────────────────────────┐
│                   CLI Controller                       │
│    (Session dispatcher, command routing, exit handler) │
└───────────────────────────┬────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
┌────────────────────────┐      ┌────────────────────────┐
│  Validation Layer      │      │  Domain & State Layer  │
│  - Table range (1-20)  │      │  - In-memory tabs O(1) │
│  - Menu matching (O(1))│◄────►│  - Item aggregation    │
│  - Quantity sanitizing │      │  - Tax & total engine  │
└────────────────────────┘      └────────────────────────┘
```

### Key Architectural Characteristics
* **In-Memory State Machine**: Tables (1–20) map to isolated order lists. Settling a table triggers an atomic state reset, freeing the table for new patrons.
* **$O(1)$ Pricing Lookups**: The menu uses a hash map (`dict`) with constant-time lookup for prices and index resolution.
* **Quantity Aggregation**: Re-ordering an existing item increments its quantity in place rather than creating duplicate row entries.
* **Pure Financial Calculation**: `calculate_bill()` operates as a deterministic function with exact decimal string formatting.

---

## Business Rules & Menu Catalog

### Menu Catalog
| Item Code | Item Name | Unit Price (INR) |
|:---:|:---|:---:|
| `1` | **Burger** | Rs. 100 |
| `2` | **Pizza**  | Rs. 200 |
| `3` | **Coffee** | Rs. 50 |

### Financial Engine
$$\text{Subtotal} = \sum_{i=1}^{n} (\text{Price}_i \times \text{Quantity}_i)$$
$$\text{Service Charge} = \text{Subtotal} \times 0.10 \quad (10\%)$$
$$\text{GST} = \text{Subtotal} \times 0.05 \quad (5\%)$$
$$\text{Grand Total} = \text{Subtotal} + \text{Service Charge} + \text{GST} = \text{Subtotal} \times 1.15$$

---

## Project Structure

```
restaurant-order-management-system/
├── restaurant_system.py       # Core application, domain logic & waiter console
├── README.md                  # System documentation & usage guide
├── summary.md                 # Technical design report & test verification
├── screenshots/               # Terminal execution captures
└── .gitignore                 # Standard Python gitignore
```

---

## Getting Started

### Prerequisites
* Python 3.7+ (Standard library only; zero external pip dependencies).

### Run the Application
Launch the waiter console from the terminal:
```bash
python restaurant_system.py
```

### Interactive Commands
* Select a table: `Table: 5`
* Add menu items: Type item name (`Burger`) or numeric index (`1`), then quantity (`2`).
* Inspect running orders: Type `order` or `view`.
* Settle and print receipt: Type `bill`.
* Finish table session: Type `done`.
* Exit console: Type `exit` or `q`.

### Example Console Session
```text
Table: 5
[Active Session: Table 5]
Order item: 1
Quantity: 2
Burger x2 added to Table 5 │ Amount: 200

Order item: 2
Quantity: 1
Pizza x1 added to Table 5 │ Amount: 200

Order item: bill
Burger x2 = 200 │ Pizza x1 = 200
Subtotal: 400 │ Service charge (10%): 40.00
GST (5%): 20.00 │ Total: 460.00

══════════════════════════════════════════════════════
               FINAL BILL RECEIPT               
══════════════════════════════════════════════════════
 Table Number : 5
──────────────────────────────────────────────────────
 Item               Qty    Price        Amount    
──────────────────────────────────────────────────────
 Burger             x2     Rs.100       Rs.200
 Pizza              x1     Rs.200       Rs.200
──────────────────────────────────────────────────────
 Subtotal: 400 │ Service charge (10%): 40.00
 GST (5%): 20.00 │ Total: 460.00
══════════════════════════════════════════════════════

Settle and clear Table 5? (y/n) [default: y]: y
Table 5 is cleared and ready for new guests.
```

---

## Verification Matrix

The system is validated across normal operations, boundary limits, tax computations, and input rejection guardrails:

| Test Scenario | Scope | Input Vector | Expected Output | Status |
|---|---|---|---|:---:|
| **Test Case 1** | Single item addition | Table `5`, Burger x2 | Amount: `200` | **PASS** |
| **Quantity Aggregation** | Re-order accumulation | Table `5`, Burger x2 + x3 | Burger x5, Amount: `500` | **PASS** |
| **Test Case 2** | Minimum / Boundary billing | Table `1`, Coffee x1 | Subtotal: `50`, Total: `57.50` | **PASS** |
| **Test Case 4** | Multi-item billing | Table `3`, Burger x2, Pizza x1, Coffee x4 | Subtotal: `600`, Total: `690.00` | **PASS** |
| **Boundary Table IDs** | Table limits | Tables `1` and `20` | Accepted | **PASS** |
| **Test Case 3 (Table)** | Range guardrails | `0`, `21`, `-1`, `"abc"` | `ValueError` raised | **PASS** |
| **Test Case 3 (Item)** | Catalog enforcement | `"pasta"`, `"tea"`, `"99"` | `ValueError` raised | **PASS** |
| **Test Case 3 (Quantity)**| Quantity checks | `0`, `-5`, `"abc"`, `"1.5"` | `ValueError` raised | **PASS** |
| **Table Reset Lifecycle** | Checkout lifecycle | Settle Table `2` | Active orders reset to `0` | **PASS** |
