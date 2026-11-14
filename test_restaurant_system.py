"""
Unit & Integration Test Suite for Restaurant Order Management System (PS No. 35)
Course: Programming Fundamentals and Logic Building Using Python (RU-100-01-0021)
Author: Aditya Soni
"""

import unittest
from restaurant_system import (
    MENU,
    TOTAL_TABLES,
    SERVICE_CHARGE_RATE,
    GST_RATE,
    table_orders,
    validate_table,
    validate_item,
    validate_quantity,
    add_order,
    get_running_order,
    format_running_order,
    calculate_bill,
    reset_table,
)


class TestRestaurantOrderSystem(unittest.TestCase):
    def setUp(self):
        # Reset all table orders before each test
        for t in range(1, TOTAL_TABLES + 1):
            reset_table(t)

    # --------------------------------------------------------------------------
    # Official Test Case 1: Normal Input
    # --------------------------------------------------------------------------
    def test_case_1_normal_input(self):
        """Test Case 1: Table 5, Item Burger (or 1), Quantity 2 -> Amount 200"""
        table = validate_table(5)
        item = validate_item("Burger")
        qty = validate_quantity(2)
        res = add_order(table, item, qty)

        self.assertEqual(res["message"], "Burger x2 added to Table 5 │ Amount: 200")
        orders = get_running_order(5)
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0]["item"], "Burger")
        self.assertEqual(orders[0]["quantity"], 2)
        self.assertEqual(orders[0]["amount"], 200)

    # --------------------------------------------------------------------------
    # Official Test Case 2: Boundary / Minimum Input
    # --------------------------------------------------------------------------
    def test_case_2_boundary_minimum_input(self):
        """Test Case 2: Table 1, Item Coffee (or 3), Quantity 1 -> Bill calculations"""
        table = validate_table(1)
        item = validate_item("Coffee")
        qty = validate_quantity(1)
        add_order(table, item, qty)

        bill = calculate_bill(1)
        self.assertEqual(bill["subtotal"], 50)
        self.assertEqual(bill["service_charge"], 5.0)
        self.assertEqual(bill["gst"], 2.5)
        self.assertEqual(bill["total"], 57.5)
        self.assertEqual(bill["line_1"], "Subtotal: 50 │ Service charge (10%): 5.00")
        self.assertEqual(bill["line_2"], "GST (5%): 2.50 │ Total: 57.50")

    # --------------------------------------------------------------------------
    # Official Test Case 3: Invalid Input Validation
    # --------------------------------------------------------------------------
    def test_case_3_invalid_inputs(self):
        """Test Case 3: Rejection of invalid table, invalid item, invalid quantity"""
        # Invalid table (0, 25, -1, non-numeric)
        with self.assertRaises(ValueError) as ctx_table:
            validate_table(0)
        self.assertIn("Invalid table number", str(ctx_table.exception))

        with self.assertRaises(ValueError) as ctx_table_high:
            validate_table(25)
        self.assertIn("Invalid table number", str(ctx_table_high.exception))

        # Invalid item ('pasta', 'sandwich')
        with self.assertRaises(ValueError) as ctx_item:
            validate_item("pasta")
        self.assertIn("Item not on the menu", str(ctx_item.exception))

        # Invalid quantity ('abc', 0, -5)
        with self.assertRaises(ValueError) as ctx_qty_str:
            validate_quantity("abc")
        self.assertIn("Invalid quantity", str(ctx_qty_str.exception))

        with self.assertRaises(ValueError) as ctx_qty_zero:
            validate_quantity(0)
        self.assertIn("Invalid quantity", str(ctx_qty_zero.exception))

    # --------------------------------------------------------------------------
    # Official Test Case 4: Different Valid Scenario (Multi-item Order)
    # --------------------------------------------------------------------------
    def test_case_4_multi_item_order_and_billing(self):
        """Test Case 4: Table 3, Burger x2, Pizza x1, Coffee x4 -> Subtotal 600, Total 690.00"""
        table = validate_table(3)
        add_order(table, validate_item("1"), validate_quantity(2))   # Burger x2 = 200
        add_order(table, validate_item("2"), validate_quantity(1))   # Pizza x1 = 200
        add_order(table, validate_item("3"), validate_quantity(4))   # Coffee x4 = 200

        running_str = format_running_order(3)
        self.assertEqual(running_str, "Burger x2 = 200 │ Pizza x1 = 200 │ Coffee x4 = 200")

        bill = calculate_bill(3)
        self.assertEqual(bill["subtotal"], 600)
        self.assertEqual(bill["service_charge"], 60.0)
        self.assertEqual(bill["gst"], 30.0)
        self.assertEqual(bill["total"], 690.0)
        self.assertEqual(bill["line_1"], "Subtotal: 600 │ Service charge (10%): 60.00")
        self.assertEqual(bill["line_2"], "GST (5%): 30.00 │ Total: 690.00")

    # --------------------------------------------------------------------------
    # Additional Verification: Table Clear & Boundary Table Numbers
    # --------------------------------------------------------------------------
    def test_boundary_table_numbers(self):
        """Verify boundary tables 1 and 20 are both accepted"""
        self.assertEqual(validate_table(1), 1)
        self.assertEqual(validate_table(20), 20)

    def test_table_clear_and_reset(self):
        """Verify table orders list is completely cleared upon checkout"""
        add_order(2, "Burger", 1)
        self.assertEqual(len(get_running_order(2)), 1)
        reset_table(2)
        self.assertEqual(len(get_running_order(2)), 0)
        self.assertEqual(format_running_order(2), "Table 2 has no active orders.")


if __name__ == "__main__":
    unittest.main()
