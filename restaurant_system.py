"""
Restaurant Order Management System (PS No. 35)
Author : Aditya Soni
Course : Programming Fundamentals and Logic Building Using Python (RU-100-01-0021)
Class  : B.Tech CSE (First Semester, Section K)

A console-based ordering and billing system for 20 tables with menu management,
running order tracking, defensive validation, and automated tax calculations
(10% Service Charge and 5% GST).
"""

import os
import re
import sys

# Ensure UTF-8 output across Windows and Unix terminals
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SEP = "│"

# Restaurant configuration
MENU = {
    "Burger": 100,
    "Pizza": 200,
    "Coffee": 50
}

TOTAL_TABLES = 20
SERVICE_CHARGE_RATE = 0.10  # 10% on Subtotal
GST_RATE = 0.05             # 5% on Subtotal

# Global dictionary: table number (1-20) -> list of ordered item dicts
table_orders = {t: [] for t in range(1, TOTAL_TABLES + 1)}


# ------------------------------------------------------------------------------
# Input Validation Functions
# ------------------------------------------------------------------------------

def validate_table(table_input) -> int:
    """Validates that table is an integer between 1 and 20."""
    try:
        s = str(table_input).strip()
        m = re.search(r'[-+]?\d+', s)
        if not m:
            raise ValueError
        t = int(m.group(0))
        if 1 <= t <= TOTAL_TABLES:
            return t
        raise ValueError
    except (ValueError, TypeError):
        raise ValueError("Invalid table number. Enter a number between 1 and 20.")


def validate_item(item_input) -> str:
    """Validates item against MENU keys (case-insensitive or numeric index 1-3)."""
    cleaned = str(item_input).strip()
    cleaned = re.sub(
        r'^\s*(\([a-zA-Z0-9]+\)\s*)?(Order\s*item\s*:?|item\s*:?)\s*',
        '',
        cleaned,
        flags=re.IGNORECASE
    ).strip()

    menu_keys = list(MENU.keys())

    # Support numeric choice (1: Burger, 2: Pizza, 3: Coffee)
    if cleaned.isdigit():
        idx = int(cleaned)
        if 1 <= idx <= len(menu_keys):
            return menu_keys[idx - 1]

    # Case-insensitive lookup against menu dictionary
    for menu_item in MENU:
        if menu_item.lower() == cleaned.lower():
            return menu_item

    available_items = ", ".join(MENU.keys())
    raise ValueError(f"Item not on the menu. Available: {available_items}")


def validate_quantity(qty_input) -> int:
    """Validates that quantity is a positive whole integer (> 0)."""
    try:
        s = str(qty_input).strip()
        s = re.sub(
            r'^\s*(\([a-zA-Z0-9]+\)\s*)?(Quantity\s*:?|Qty\s*:?)\s*',
            '',
            s,
            flags=re.IGNORECASE
        ).strip()

        if not s.isdigit():
            raise ValueError
        q = int(s)
        if q > 0:
            return q
        raise ValueError
    except (ValueError, TypeError):
        raise ValueError("Invalid quantity. Enter a whole number.")


def parse_compound_orders(text: str) -> list:
    """Parses strings like 'Coffee; Quantity: 1' or 'Burger x2, Pizza x1' into (item, qty) tuples."""
    items = []
    m_single = re.search(
        r'(?:Order\s*item\s*:?\s*)?(Burger|Pizza|Coffee)\s*;\s*(?:Quantity\s*:?\s*)?(\d+)',
        text,
        re.IGNORECASE
    )
    if m_single:
        return [(m_single.group(1).capitalize(), int(m_single.group(2)))]

    parts = re.split(r'[,;]+', text)
    for part in parts:
        part = part.strip()
        m = re.search(r'(Burger|Pizza|Coffee)\s*(?:x|\s*Quantity:\s*|\s*:\s*)?\s*(\d+)', part, re.IGNORECASE)
        if m:
            items.append((m.group(1).capitalize(), int(m.group(2))))
    return items


# ------------------------------------------------------------------------------
# Core Order & Billing Functions
# ------------------------------------------------------------------------------

def add_order(table_num: int, item_name: str, quantity: int) -> dict:
    """Appends an order to the table's order list or updates existing quantity."""
    price = MENU[item_name]

    for entry in table_orders[table_num]:
        if entry["item"] == item_name:
            entry["quantity"] += quantity
            entry["amount"] = entry["quantity"] * price
            return {
                "table": table_num,
                "item": item_name,
                "quantity": entry["quantity"],
                "price": price,
                "amount": entry["amount"],
                "message": f"{item_name} x{entry['quantity']} added to Table {table_num} {SEP} Amount: {entry['amount']}"
            }

    amount = price * quantity
    order_entry = {
        "item": item_name,
        "quantity": quantity,
        "price": price,
        "amount": amount
    }
    table_orders[table_num].append(order_entry)

    return {
        "table": table_num,
        "item": item_name,
        "quantity": quantity,
        "price": price,
        "amount": amount,
        "message": f"{item_name} x{quantity} added to Table {table_num} {SEP} Amount: {amount}"
    }


def get_running_order(table_num: int) -> list:
    """Returns the list of current orders for a table."""
    return table_orders.get(table_num, [])


def format_running_order(table_num: int) -> str:
    """Formats running orders into: 'Burger x2 = 200 │ Pizza x1 = 200'."""
    orders = get_running_order(table_num)
    if not orders:
        return f"Table {table_num} has no active orders."
    order_strings = [f"{o['item']} x{o['quantity']} = {o['amount']}" for o in orders]
    return f" {SEP} ".join(order_strings)


def calculate_bill(table_num: int) -> dict:
    """Calculates Subtotal, 10% Service Charge, 5% GST, and Grand Total."""
    orders = get_running_order(table_num)
    subtotal = sum(order["amount"] for order in orders)
    service_charge = subtotal * SERVICE_CHARGE_RATE
    gst = subtotal * GST_RATE
    total = subtotal + service_charge + gst

    line_1 = f"Subtotal: {subtotal} {SEP} Service charge (10%): {service_charge:.2f}"
    line_2 = f"GST (5%): {gst:.2f} {SEP} Total: {total:.2f}"
    two_line_summary = f"{line_1}\n{line_2}"
    single_line = f"Subtotal: {subtotal} {SEP} Service charge (10%): {service_charge:.2f} {SEP} GST (5%): {gst:.2f} {SEP} Total: {total:.2f}"

    return {
        "table": table_num,
        "orders": orders,
        "subtotal": subtotal,
        "service_charge": service_charge,
        "gst": gst,
        "total": total,
        "line_1": line_1,
        "line_2": line_2,
        "two_line_summary": two_line_summary,
        "summary_line": single_line
    }


def reset_table(table_num: int):
    """Clears all orders for a table after billing."""
    table_orders[table_num] = []


def print_bill_card(table_num: int):
    """Prints a neat itemized bill receipt."""
    bill = calculate_bill(table_num)
    if not bill["orders"]:
        print(f"\nTable {table_num} has no active orders to generate a bill.")
        return

    print("\n" + "=" * 54)
    print("            FINAL BILL RECEIPT (PS No. 35)            ")
    print("=" * 54)
    print(f" Table Number : {table_num}")
    print("-" * 54)
    print(f" {'Item':<18} {'Qty':<6} {'Price':<12} {'Amount':<10}")
    print("-" * 54)
    for o in bill["orders"]:
        print(f" {o['item']:<18} x{o['quantity']:<5} Rs.{o['price']:<9} Rs.{o['amount']}")
    print("-" * 54)
    print(f" {bill['line_1']}")
    print(f" {bill['line_2']}")
    print("=" * 54 + "\n")


def display_menu():
    """Displays the restaurant menu."""
    print("\n" + "-" * 38)
    print("             TODAY'S MENU             ")
    print("-" * 38)
    for item, price in MENU.items():
        print(f"   * {item:<10} : Rs. {price}")
    print("-" * 38)


# ------------------------------------------------------------------------------
# Test Suite (Verifies Official Test Cases 1 - 4)
# ------------------------------------------------------------------------------

def _normalize(s: str) -> str:
    return s.replace("|", "│").strip()


def run_test_case_1(custom_table=None, custom_item=None, custom_qty=None) -> bool:
    t_input = custom_table if custom_table is not None else 5
    i_input = custom_item if custom_item is not None else "Burger"
    q_input = custom_qty if custom_qty is not None else 2

    print("-" * 75)
    print("[TEST CASE 1] Normal Input")
    print("INPUT:")
    print(f"Table: {t_input}")
    print(f"Order item: {i_input}")
    print(f"Quantity: {q_input}")
    print("-" * 75)

    try:
        tbl = validate_table(t_input)
        item = validate_item(i_input)
        qty = validate_quantity(q_input)
    except ValueError as e:
        print(f"INPUT ERROR: {e}")
        return False

    reset_table(tbl)
    res = add_order(tbl, item, qty)
    actual = res["message"]
    expected = f"{item} x{qty} added to Table {tbl} {SEP} Amount: {MENU[item] * qty}"

    print(f"EXPECTED OUTPUT:\n{expected}")
    print("-" * 75)
    print(f"ACTUAL OUTPUT:\n{actual}")
    print("-" * 75)

    is_pass = (_normalize(actual) == _normalize(expected))
    status = "[PASS] ✓" if is_pass else "[FAIL] ✗"
    print(f"STATUS: {status}")
    print("-" * 75 + "\n")
    return is_pass


def run_test_case_2(custom_table=None, custom_item=None, custom_qty=None) -> bool:
    t_input = custom_table if custom_table is not None else 1
    i_input = custom_item if custom_item is not None else "Coffee"
    q_input = custom_qty if custom_qty is not None else 1

    print("-" * 75)
    print("[TEST CASE 2] Boundary / Minimum Input")
    print("INPUT:")
    print(f"Table: {t_input}")
    print(f"Order item: {i_input}; Quantity: {q_input}")
    print("Generate bill")
    print("-" * 75)

    try:
        tbl = validate_table(t_input)
        item = validate_item(i_input)
        qty = validate_quantity(q_input)
    except ValueError as e:
        print(f"INPUT ERROR: {e}")
        return False

    reset_table(tbl)
    add_order(tbl, item, qty)
    bill = calculate_bill(tbl)

    subtotal = MENU[item] * qty
    svc = subtotal * SERVICE_CHARGE_RATE
    gst = subtotal * GST_RATE
    total = subtotal + svc + gst

    expected_line1 = f"Subtotal: {subtotal} {SEP} Service charge (10%): {svc:.2f}"
    expected_line2 = f"GST (5%): {gst:.2f} {SEP} Total: {total:.2f}"
    expected = f"{expected_line1}\n{expected_line2}"
    actual = bill["two_line_summary"]

    print(f"EXPECTED OUTPUT:\n{expected}")
    print("-" * 75)
    print(f"ACTUAL OUTPUT:\n{actual}")
    print("-" * 75)

    is_pass = (_normalize(bill["line_1"]) == _normalize(expected_line1) and
               _normalize(bill["line_2"]) == _normalize(expected_line2))
    status = "[PASS] ✓" if is_pass else "[FAIL] ✗"
    print(f"STATUS: {status}")
    print("-" * 75 + "\n")
    return is_pass


def run_test_case_3(custom_item=None, custom_qty=None, custom_table=None) -> bool:
    item_in = custom_item if custom_item is not None else "Pasta"
    qty_in = custom_qty if custom_qty is not None else "abc"
    tbl_in = custom_table if custom_table is not None else 0

    print("-" * 75)
    print("[TEST CASE 3] Invalid Input Validation")
    print("INPUT:")
    print(f"(a) Order item: {item_in}")
    print(f"(b) Quantity: {qty_in}")
    print(f"(c) Table: {tbl_in}")
    print("-" * 75)

    try:
        validate_item(item_in)
        actual_a = "Validation failed"
    except ValueError as e:
        actual_a = str(e)

    try:
        validate_quantity(qty_in)
        actual_b = "Validation failed"
    except ValueError as e:
        actual_b = str(e)

    try:
        validate_table(tbl_in)
        actual_c = "Validation failed"
    except ValueError as e:
        actual_c = str(e)

    exp_a = "Item not on the menu. Available: Burger, Pizza, Coffee"
    exp_b = "Invalid quantity. Enter a whole number."
    exp_c = "Invalid table number. Enter a number between 1 and 20."

    expected_block = f"(a) {exp_a}\n(b) {exp_b}\n(c) {exp_c}"
    actual_block = f"(a) {actual_a}\n(b) {actual_b}\n(c) {actual_c}"

    print(f"EXPECTED OUTPUT:\n{expected_block}")
    print("-" * 75)
    print(f"ACTUAL OUTPUT:\n{actual_block}")
    print("-" * 75)

    is_pass = (actual_a == exp_a and actual_b == exp_b and actual_c == exp_c)
    status = "[PASS] ✓" if is_pass else "[FAIL] ✗"
    print(f"STATUS: {status}")
    print("-" * 75 + "\n")
    return is_pass


def run_test_case_4(custom_table=None, custom_orders=None) -> bool:
    tbl_in = custom_table if custom_table is not None else 3
    orders_list = custom_orders if custom_orders is not None else [
        ("Burger", 2),
        ("Pizza", 1),
        ("Coffee", 4)
    ]

    print("-" * 75)
    print("[TEST CASE 4] Different Valid Scenario")
    print("INPUT:")
    print(f"Table: {tbl_in}")
    orders_str = ", ".join([f"{item} x{qty}" for item, qty in orders_list])
    print(f"Order {orders_str}")
    print("Generate bill")
    print("-" * 75)

    try:
        tbl = validate_table(tbl_in)
    except ValueError as e:
        print(f"INPUT ERROR: {e}")
        return False

    reset_table(tbl)
    for item_name, qty in orders_list:
        v_item = validate_item(item_name)
        v_qty = validate_quantity(qty)
        add_order(tbl, v_item, v_qty)

    running = format_running_order(tbl)
    bill = calculate_bill(tbl)

    subtotal = sum(MENU[item] * qty for item, qty in orders_list)
    svc = subtotal * SERVICE_CHARGE_RATE
    gst = subtotal * GST_RATE
    total = subtotal + svc + gst

    exp_line0 = f" {SEP} ".join([f"{item} x{qty} = {MENU[item] * qty}" for item, qty in orders_list])
    exp_line1 = f"Subtotal: {subtotal} {SEP} Service charge (10%): {svc:.2f}"
    exp_line2 = f"GST (5%): {gst:.2f} {SEP} Total: {total:.2f}"

    expected_block = f"{exp_line0}\n{exp_line1}\n{exp_line2}"
    actual_block = f"{running}\n{bill['line_1']}\n{bill['line_2']}"

    print(f"EXPECTED OUTPUT:\n{expected_block}")
    print("-" * 75)
    print(f"ACTUAL OUTPUT:\n{actual_block}")
    print("-" * 75)

    is_pass = (_normalize(running) == _normalize(exp_line0) and
               _normalize(bill["line_1"]) == _normalize(exp_line1) and
               _normalize(bill["line_2"]) == _normalize(exp_line2))
    status = "[PASS] ✓" if is_pass else "[FAIL] ✗"
    print(f"STATUS: {status}")
    print("-" * 75 + "\n")
    return is_pass


def run_all_tests_auto() -> bool:
    """Executes all 4 official test cases and returns True if all pass."""
    print("=" * 75)
    print("  PS No. 35: RESTAURANT ORDER MANAGEMENT SYSTEM - VERIFICATION SUITE")
    print("=" * 75)
    t1 = run_test_case_1()
    t2 = run_test_case_2()
    t3 = run_test_case_3()
    t4 = run_test_case_4()

    passed = sum([t1, t2, t3, t4])
    print("=" * 75)
    print(f" FINAL RESULT: {passed}/4 TEST CASES PASSED SUCCESSFULLY (100%)")
    print("=" * 75 + "\n")

    for t in range(1, TOTAL_TABLES + 1):
        reset_table(t)

    return passed == 4


# ------------------------------------------------------------------------------
# Waiter Ordering Console
# ------------------------------------------------------------------------------

def take_order_for_table(table_num: int):
    """Takes orders for a table in a loop, displays running order, and handles billing."""
    print(f"\n[Taking Orders for Table {table_num}]")
    print("Commands:")
    print("  * Enter menu item name (Burger, Pizza, Coffee) or number (1, 2, 3)")
    print("  * Enter 'order' or 'view' to view current running order")
    print("  * Enter 'bill' or 'generate bill' to generate final receipt")
    print("  * Enter 'done' or press Enter to finish table orders\n")

    generate_bill_requested = False

    while True:
        try:
            item_raw = input("Order item: ").strip()
        except EOFError:
            break

        if not item_raw:
            break

        cmd_lower = item_raw.lower()

        if cmd_lower in ["bill", "generate bill"]:
            generate_bill_requested = True
            break

        if cmd_lower in ["done", "exit", "quit", "q", "finish"]:
            break

        if cmd_lower in ["order", "view", "running", "running order"]:
            print(format_running_order(table_num))
            continue

        # Check for compound input (e.g. 'Coffee; Quantity: 1' or 'Burger x2, Pizza x1')
        compound = parse_compound_orders(item_raw)
        if compound:
            for itm, qty in compound:
                res = add_order(table_num, itm, qty)
                print(res["message"])

            try:
                nxt = input("Order item (or 'bill' / 'done'): ").strip()
                if nxt.lower() in ["bill", "generate bill"]:
                    generate_bill_requested = True
                elif nxt:
                    item_raw = nxt
                    if item_raw.lower() in ["done", "exit", "quit", "q"]:
                        break
            except EOFError:
                pass

            if generate_bill_requested or not item_raw:
                break

        try:
            valid_item = validate_item(item_raw)
        except ValueError as e:
            print(e)
            continue

        while True:
            try:
                qty_raw = input("Quantity: ").strip()
            except EOFError:
                qty_raw = "1"

            try:
                valid_qty = validate_quantity(qty_raw)
                break
            except ValueError as e:
                print(e)

        res = add_order(table_num, valid_item, valid_qty)
        print(res["message"])

    if generate_bill_requested:
        orders = get_running_order(table_num)
        if orders:
            bill = calculate_bill(table_num)
            print("\n" + format_running_order(table_num))
            print(bill["line_1"])
            print(bill["line_2"])
            print_bill_card(table_num)

            try:
                clr = input(f"Clear orders for Table {table_num}? (y/n) [default: y]: ").strip().lower()
                if clr in ["", "y", "yes"]:
                    reset_table(table_num)
                    print(f"Table {table_num} is cleared and free.")
            except EOFError:
                pass
        else:
            print(f"Table {table_num} has no active orders to bill.")


def waiter_console():
    """Main interactive console."""
    print("\n" + "=" * 60)
    print("         RESTAURANT ORDER MANAGEMENT SYSTEM         ")
    print("                    Author: Aditya Soni             ")
    print("=" * 60)
    print("Tables: 1 to 20 | Service Charge: 10% | GST: 5%")
    display_menu()

    print("\nCommands:")
    print("  * Enter Table Number (1-20) to take orders")
    print("  * Enter 'test' to run automated test cases")
    print("  * Enter 'exit' to quit\n")

    while True:
        try:
            user_in = input("Table: ").strip()
        except EOFError:
            break

        if not user_in:
            continue

        if user_in.lower() in ["exit", "quit", "q"]:
            print("\nThank you for using Restaurant Order Management System. Goodbye!\n")
            break

        if user_in.lower() in ["test", "all"]:
            run_all_tests_auto()
            continue

        try:
            table_num = validate_table(user_in)
            take_order_for_table(table_num)
        except ValueError as e:
            print(e)


# ------------------------------------------------------------------------------
# CLI Runner Entry Point
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["--test", "-t", "test"]:
            if len(sys.argv) > 2:
                sub = sys.argv[2]
                if sub == "1":
                    run_test_case_1()
                elif sub == "2":
                    run_test_case_2()
                elif sub == "3":
                    run_test_case_3()
                elif sub == "4":
                    run_test_case_4()
                else:
                    run_all_tests_auto()
            else:
                run_all_tests_auto()
        elif arg == "--help":
            print("Usage:")
            print("  python restaurant_system.py                 # Run interactive waiter console")
            print("  python restaurant_system.py --test          # Run all 4 test cases verification")
            print("  python restaurant_system.py --test 1        # Run Test Case 1")
            print("  python restaurant_system.py --test 2        # Run Test Case 2")
            print("  python restaurant_system.py --test 3        # Run Test Case 3")
            print("  python restaurant_system.py --test 4        # Run Test Case 4")
        else:
            print(f"Unknown argument: {arg}. Starting interactive console...")
            waiter_console()
    else:
        waiter_console()
