"""
Restaurant Order Management System (PS-35)
Console-based order dispatch, state management, and automated tax billing engine.

Architecture:
  - In-memory state with O(1) item lookups and isolated table order collections.
  - Decoupled domain calculations, defensive input filters, and presentation layer.
"""

from __future__ import annotations

import sys
from typing import Dict, List, Optional, TypedDict


# Ensure UTF-8 output across standard Windows and Unix terminals
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DELIMITER = "│"

# Core Menu & Business Rates
MENU: Dict[str, int] = {
    "Burger": 100,
    "Pizza": 200,
    "Coffee": 50,
}

TOTAL_TABLES: int = 20
SERVICE_CHARGE_RATE: float = 0.10  # 10% on Subtotal
GST_RATE: float = 0.05             # 5% on Subtotal


class OrderRecord(TypedDict):
    item: str
    quantity: int
    price: int
    amount: int


class BillBreakdown(TypedDict):
    orders: List[OrderRecord]
    subtotal: int
    service_charge: float
    gst: float
    total: float
    line_1: str
    line_2: str


# In-memory table order store (Tables 1 through 20)
table_orders: Dict[int, List[OrderRecord]] = {
    table_id: [] for table_id in range(1, TOTAL_TABLES + 1)
}


# ==============================================================================
# Input Validation & Sanitization Filters
# ==============================================================================

def validate_table(table_input: object) -> int:
    """
    Validates and normalizes table input.

    Raises:
        ValueError: If table number is not an integer in range [1, TOTAL_TABLES].
    """
    try:
        table_number = int(str(table_input).strip())
        if 1 <= table_number <= TOTAL_TABLES:
            return table_number
        raise ValueError
    except (ValueError, TypeError):
        raise ValueError(f"Invalid table number. Enter a number between 1 and {TOTAL_TABLES}.")


def validate_item(item_input: object) -> str:
    """
    Validates and resolves menu item by name (case-insensitive) or menu index.

    Raises:
        ValueError: If item is not found in MENU.
    """
    raw_query = str(item_input).strip()
    available_items = list(MENU.keys())

    # Support numeric menu index selection (1-indexed)
    if raw_query.isdigit():
        index = int(raw_query)
        if 1 <= index <= len(available_items):
            return available_items[index - 1]

    # Case-insensitive string match
    normalized_query = raw_query.lower()
    for item_name in MENU:
        if item_name.lower() == normalized_query:
            return item_name

    available_list = ", ".join(MENU.keys())
    raise ValueError(f"Item not on the menu. Available: {available_list}")


def validate_quantity(quantity_input: object) -> int:
    """
    Validates that quantity is a strictly positive whole integer.

    Raises:
        ValueError: If quantity is non-numeric, decimal, or <= 0.
    """
    try:
        raw_str = str(quantity_input).strip()
        if not raw_str.isdigit():
            raise ValueError
        parsed_qty = int(raw_str)
        if parsed_qty > 0:
            return parsed_qty
        raise ValueError
    except (ValueError, TypeError):
        raise ValueError("Invalid quantity. Enter a whole number.")


# ==============================================================================
# Domain & State Management Engine
# ==============================================================================

def add_order(table_num: int, item_name: str, quantity: int) -> Dict[str, str]:
    """
    Adds an order item to a table's running tab.
    Aggregates quantity and updates amount if the item was already ordered.
    """
    unit_price = MENU[item_name]

    # Aggregate if item is already in this table's order list
    for entry in table_orders[table_num]:
        if entry["item"] == item_name:
            entry["quantity"] += quantity
            entry["amount"] = entry["quantity"] * unit_price
            return {
                "message": (
                    f"{item_name} x{entry['quantity']} added to Table {table_num} "
                    f"{DELIMITER} Amount: {entry['amount']}"
                )
            }

    # Append fresh order entry
    total_amount = unit_price * quantity
    new_entry: OrderRecord = {
        "item": item_name,
        "quantity": quantity,
        "price": unit_price,
        "amount": total_amount,
    }
    table_orders[table_num].append(new_entry)

    return {
        "message": (
            f"{item_name} x{quantity} added to Table {table_num} "
            f"{DELIMITER} Amount: {total_amount}"
        )
    }


def get_running_order(table_num: int) -> List[OrderRecord]:
    """Retrieves current unbilled orders for the specified table."""
    return table_orders.get(table_num, [])


def format_running_order(table_num: int) -> str:
    """Formats running orders into a human-readable delimited string."""
    orders = get_running_order(table_num)
    if not orders:
        return f"Table {table_num} has no active orders."

    return f" {DELIMITER} ".join(
        f"{entry['item']} x{entry['quantity']} = {entry['amount']}"
        for entry in orders
    )


def calculate_bill(table_num: int) -> BillBreakdown:
    """
    Computes financial breakdown for a table:
      - Subtotal: Sum of (price * quantity)
      - Service Charge: 10% of Subtotal
      - GST: 5% of Subtotal
      - Total: Subtotal + Service Charge + GST
    """
    orders = get_running_order(table_num)
    subtotal = sum(entry["amount"] for entry in orders)
    service_charge = subtotal * SERVICE_CHARGE_RATE
    gst = subtotal * GST_RATE
    total = subtotal + service_charge + gst

    return {
        "orders": orders,
        "subtotal": subtotal,
        "service_charge": service_charge,
        "gst": gst,
        "total": total,
        "line_1": f"Subtotal: {subtotal} {DELIMITER} Service charge (10%): {service_charge:.2f}",
        "line_2": f"GST (5%): {gst:.2f} {DELIMITER} Total: {total:.2f}",
    }


def reset_table(table_num: int) -> None:
    """Clears all orders for a table upon bill settlement."""
    table_orders[table_num] = []


# ==============================================================================
# Presentation & CLI Formatting
# ==============================================================================

def display_menu() -> None:
    """Renders the current menu and item prices in a clean tabular format."""
    print("\n" + "─" * 38)
    print("             TODAY'S MENU             ")
    print("─" * 38)
    for idx, (item, price) in enumerate(MENU.items(), start=1):
        print(f"  {idx}. {item:<14} : Rs. {price}")
    print("─" * 38)


def print_bill_card(table_num: int) -> None:
    """Renders a structured, formatted receipt card to stdout."""
    bill = calculate_bill(table_num)
    if not bill["orders"]:
        print(f"\nTable {table_num} has no active orders to generate a bill.")
        return

    print("\n" + "═" * 54)
    print("               FINAL BILL RECEIPT               ")
    print("═" * 54)
    print(f" Table Number : {table_num}")
    print("─" * 54)
    print(f" {'Item':<18} {'Qty':<6} {'Price':<12} {'Amount':<10}")
    print("─" * 54)
    for entry in bill["orders"]:
        print(
            f" {entry['item']:<18} x{entry['quantity']:<5} "
            f"Rs.{entry['price']:<9} Rs.{entry['amount']}"
        )
    print("─" * 54)
    print(f" {bill['line_1']}")
    print(f" {bill['line_2']}")
    print("═" * 54 + "\n")


# ==============================================================================
# Waiter Console Dispatcher
# ==============================================================================

def take_order_for_table(table_num: int) -> None:
    """Manages the interactive ordering session for a given table."""
    print(f"\n[Active Session: Table {table_num}]")
    print("Commands:")
    print("  • Item name or menu index (1: Burger, 2: Pizza, 3: Coffee)")
    print("  • 'order' / 'view' : Review current running order")
    print("  • 'bill'           : Compute taxes and print receipt")
    print("  • 'done'           : Exit table session\n")

    generate_bill_requested = False

    while True:
        try:
            item_raw = input("Order item: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSession interrupted.")
            break

        if not item_raw:
            break

        cmd = item_raw.lower()

        if cmd in ("bill", "generate bill"):
            generate_bill_requested = True
            break

        if cmd in ("done", "exit", "quit", "finish"):
            break

        if cmd in ("order", "view", "running", "running order"):
            print(format_running_order(table_num))
            continue

        try:
            valid_item = validate_item(item_raw)
        except ValueError as err:
            print(err)
            continue

        while True:
            try:
                qty_raw = input("Quantity: ").strip()
            except (EOFError, KeyboardInterrupt):
                qty_raw = "1"

            try:
                valid_qty = validate_quantity(qty_raw)
                break
            except ValueError as err:
                print(err)

        result = add_order(table_num, valid_item, valid_qty)
        print(result["message"])

    if generate_bill_requested:
        if get_running_order(table_num):
            bill = calculate_bill(table_num)
            print("\n" + format_running_order(table_num))
            print(bill["line_1"])
            print(bill["line_2"])
            print_bill_card(table_num)

            try:
                prompt = input(f"Settle and clear Table {table_num}? (y/n) [default: y]: ").strip().lower()
                if prompt in ("", "y", "yes"):
                    reset_table(table_num)
                    print(f"Table {table_num} is cleared and ready for new guests.")
            except (EOFError, KeyboardInterrupt):
                pass
        else:
            print(f"Table {table_num} has no active orders to bill.")


def main() -> None:
    """Console application entry point."""
    print("\n" + "═" * 54)
    print("        RESTAURANT ORDER MANAGEMENT SYSTEM        ")
    print("               Production Console                 ")
    print("═" * 54)
    display_menu()

    while True:
        try:
            user_input = input("\nTable: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nShutdown signal received. Exiting.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit", "q"):
            print("\nThank you for using Restaurant Order Management System. Goodbye!\n")
            break

        try:
            table_number = validate_table(user_input)
            take_order_for_table(table_number)
        except ValueError as err:
            print(err)


if __name__ == "__main__":
    main()
