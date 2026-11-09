"""
Restaurant Order Management System
Author : Aditya Soni
Course : Programming Fundamentals and Logic Building Using Python (RU-100-01-0021)
Class  : B.Tech CSE (First Semester, Section K)
Problem Statement : PS No. 35
"""

import sys

# Ensure UTF-8 output across all consoles
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Separator for neat console output
SEP = "│"

# Requirement 2: Menu stored in a Dictionary
MENU = {
    "Burger": 100,
    "Pizza": 200,
    "Coffee": 50
}

TOTAL_TABLES = 20
SERVICE_CHARGE_RATE = 0.10  # 10% on Subtotal
GST_RATE = 0.05             # 5% on Subtotal

# Requirement 2: Ordered items for each table stored in a List
table_orders = {t: [] for t in range(1, TOTAL_TABLES + 1)}


# ------------------------------------------------------------------------------
# Requirement 5: Input Validation Functions
# ------------------------------------------------------------------------------

def validate_table(table_input) -> int:
    """Validates that table number is an integer between 1 and 20."""
    try:
        t = int(str(table_input).strip())
        if 1 <= t <= TOTAL_TABLES:
            return t
        raise ValueError
    except (ValueError, TypeError):
        raise ValueError("Invalid table number. Enter a number between 1 and 20.")


def validate_item(item_input) -> str:
    """Validates that the item is on the menu (case-insensitive or by index 1-3)."""
    cleaned = str(item_input).strip()
    menu_keys = list(MENU.keys())

    # Support selecting by menu number (1: Burger, 2: Pizza, 3: Coffee)
    if cleaned.isdigit():
        idx = int(cleaned)
        if 1 <= idx <= len(menu_keys):
            return menu_keys[idx - 1]

    # Case-insensitive matching with menu items
    for item in MENU:
        if item.lower() == cleaned.lower():
            return item

    available = ", ".join(MENU.keys())
    raise ValueError(f"Item not on the menu. Available: {available}")


def validate_quantity(qty_input) -> int:
    """Validates that quantity is a positive whole integer (> 0)."""
    try:
        s = str(qty_input).strip()
        if not s.isdigit():
            raise ValueError
        q = int(s)
        if q > 0:
            return q
        raise ValueError
    except (ValueError, TypeError):
        raise ValueError("Invalid quantity. Enter a whole number.")


# ------------------------------------------------------------------------------
# Core Order & Billing Functions
# ------------------------------------------------------------------------------

def display_menu():
    """Prints the current restaurant menu and prices."""
    print("\n" + "-" * 36)
    print("            TODAY'S MENU            ")
    print("-" * 36)
    for idx, (item, price) in enumerate(MENU.items(), start=1):
        print(f"  {idx}. {item:<12} : Rs. {price}")
    print("-" * 36)


def add_order(table_num: int, item_name: str, quantity: int) -> dict:
    """
    Requirement 2 & 3:
    Adds an ordered item to the table's list. If already ordered, updates quantity.
    """
    price = MENU[item_name]

    # If item already exists in this table's order list, update quantity
    for order in table_orders[table_num]:
        if order["item"] == item_name:
            order["quantity"] += quantity
            order["amount"] = order["quantity"] * price
            return {
                "message": f"{item_name} x{order['quantity']} added to Table {table_num} {SEP} Amount: {order['amount']}"
            }

    # Otherwise, create a new order entry
    amount = price * quantity
    order_entry = {
        "item": item_name,
        "quantity": quantity,
        "price": price,
        "amount": amount
    }
    table_orders[table_num].append(order_entry)

    return {
        "message": f"{item_name} x{quantity} added to Table {table_num} {SEP} Amount: {amount}"
    }


def get_running_order(table_num: int) -> list:
    """Returns the list of current orders for a table."""
    return table_orders.get(table_num, [])


def format_running_order(table_num: int) -> str:
    """
    Requirement 3:
    Formats the running order into a readable string: 'Burger x2 = 200 │ Pizza x1 = 200'
    """
    orders = get_running_order(table_num)
    if not orders:
        return f"Table {table_num} has no active orders."
    return f" {SEP} ".join([f"{o['item']} x{o['quantity']} = {o['amount']}" for o in orders])


def calculate_bill(table_num: int) -> dict:
    """
    Requirement 4:
    Calculates Subtotal, 10% Service Charge, 5% GST, and Grand Total.
    """
    orders = get_running_order(table_num)
    subtotal = sum(order["amount"] for order in orders)
    service_charge = subtotal * SERVICE_CHARGE_RATE
    gst = subtotal * GST_RATE
    total = subtotal + service_charge + gst

    line_1 = f"Subtotal: {subtotal} {SEP} Service charge (10%): {service_charge:.2f}"
    line_2 = f"GST (5%): {gst:.2f} {SEP} Total: {total:.2f}"

    return {
        "orders": orders,
        "subtotal": subtotal,
        "service_charge": service_charge,
        "gst": gst,
        "total": total,
        "line_1": line_1,
        "line_2": line_2
    }


def print_bill_card(table_num: int):
    """Requirement 4: Prints a formatted bill receipt for the table."""
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


def reset_table(table_num: int):
    """Clears all orders for a table after billing is complete."""
    table_orders[table_num] = []


# ------------------------------------------------------------------------------
# Requirement 1 & 3: Waiter Console Workflow
# ------------------------------------------------------------------------------

def take_order_for_table(table_num: int):
    """
    Requirement 3:
    Runs a loop to take multiple orders for a table, views running orders,
    and generates the final bill when requested.
    """
    print(f"\n[Taking Orders for Table {table_num}]")
    print("Commands:")
    print("  * Enter menu item name (Burger, Pizza, Coffee) or number (1, 2, 3)")
    print("  * Enter 'order' or 'view' to view current running order")
    print("  * Enter 'bill' to generate final receipt")
    print("  * Enter 'done' to finish table orders\n")

    generate_bill_requested = False

    while True:
        try:
            item_raw = input("Order item: ").strip()
        except EOFError:
            break

        if not item_raw:
            break

        cmd = item_raw.lower()

        # Handle bill request
        if cmd in ["bill", "generate bill"]:
            generate_bill_requested = True
            break

        # Handle finish without billing
        if cmd in ["done", "exit", "quit", "finish"]:
            break

        # Handle view running order
        if cmd in ["order", "view", "running", "running order"]:
            print(format_running_order(table_num))
            continue

        # Validate menu item
        try:
            valid_item = validate_item(item_raw)
        except ValueError as e:
            print(e)
            continue

        # Validate quantity
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

        # Add order and show confirmation
        res = add_order(table_num, valid_item, valid_qty)
        print(res["message"])

    # Generate bill if requested
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


def main():
    """Main waiter console entry point."""
    print("\n" + "=" * 54)
    print("       RESTAURANT ORDER MANAGEMENT SYSTEM       ")
    print("               Author: Aditya Soni              ")
    print("=" * 54)
    display_menu()

    while True:
        try:
            user_in = input("\nTable: ").strip()
        except EOFError:
            break

        if not user_in:
            continue

        if user_in.lower() in ["exit", "quit", "q"]:
            print("\nThank you for using Restaurant Order Management System. Goodbye!\n")
            break

        try:
            table_num = validate_table(user_in)
            take_order_for_table(table_num)
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()
