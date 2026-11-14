"""
Automated Test Suite for Restaurant Order Management System
Tests domain models, input sanitation guards, state aggregation, and tax calculation.
"""

import unittest
from restaurant_system import (
    TOTAL_TABLES,
    add_order,
    calculate_bill,
    format_running_order,
    get_running_order,
    reset_table,
    validate_item,
    validate_quantity,
    validate_table,
)


class TestRestaurantOrderSystem(unittest.TestCase):
    """Integration and unit tests for order processing and financial calculation."""

    def setUp(self) -> None:
        """Reset all table tabs before each test execution."""
        for table_id in range(1, TOTAL_TABLES + 1):
            reset_table(table_id)

    def test_order_addition_and_item_state(self) -> None:
        """Verify normal single-item order correctly appends and computes line amount."""
        table = validate_table(5)
        item = validate_item("Burger")
        qty = validate_quantity(2)
        response = add_order(table, item, qty)

        self.assertEqual(response["message"], "Burger x2 added to Table 5 │ Amount: 200")
        orders = get_running_order(5)
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0]["item"], "Burger")
        self.assertEqual(orders[0]["quantity"], 2)
        self.assertEqual(orders[0]["price"], 100)
        self.assertEqual(orders[0]["amount"], 200)

    def test_order_aggregation_for_duplicate_items(self) -> None:
        """Verify adding an existing item aggregates quantity instead of duplicating entries."""
        add_order(5, "Burger", 2)
        add_order(5, "Burger", 3)

        orders = get_running_order(5)
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0]["quantity"], 5)
        self.assertEqual(orders[0]["amount"], 500)

    def test_bill_calculation_rates_and_formatting(self) -> None:
        """Verify subtotal, 10% service charge, 5% GST, and grand total calculations."""
        table = validate_table(1)
        item = validate_item("Coffee")
        qty = validate_quantity(1)
        add_order(table, item, qty)

        bill = calculate_bill(1)
        self.assertEqual(bill["subtotal"], 50)
        self.assertAlmostEqual(bill["service_charge"], 5.00, places=2)
        self.assertAlmostEqual(bill["gst"], 2.50, places=2)
        self.assertAlmostEqual(bill["total"], 57.50, places=2)
        self.assertEqual(bill["line_1"], "Subtotal: 50 │ Service charge (10%): 5.00")
        self.assertEqual(bill["line_2"], "GST (5%): 2.50 │ Total: 57.50")

    def test_multi_item_order_subtotal_and_tax_aggregation(self) -> None:
        """Verify multi-item order aggregation and cumulative financial calculations."""
        table = validate_table(3)
        add_order(table, validate_item("1"), validate_quantity(2))  # Burger x2 = 200
        add_order(table, validate_item("2"), validate_quantity(1))  # Pizza x1 = 200
        add_order(table, validate_item("3"), validate_quantity(4))  # Coffee x4 = 200

        running_str = format_running_order(3)
        self.assertEqual(
            running_str,
            "Burger x2 = 200 │ Pizza x1 = 200 │ Coffee x4 = 200",
        )

        bill = calculate_bill(3)
        self.assertEqual(bill["subtotal"], 600)
        self.assertAlmostEqual(bill["service_charge"], 60.00, places=2)
        self.assertAlmostEqual(bill["gst"], 30.00, places=2)
        self.assertAlmostEqual(bill["total"], 690.00, places=2)
        self.assertEqual(bill["line_1"], "Subtotal: 600 │ Service charge (10%): 60.00")
        self.assertEqual(bill["line_2"], "GST (5%): 30.00 │ Total: 690.00")

    def test_boundary_table_numbers(self) -> None:
        """Verify boundary table IDs (1 and 20) are accepted."""
        self.assertEqual(validate_table(1), 1)
        self.assertEqual(validate_table(20), 20)
        self.assertEqual(validate_table(" 1 "), 1)
        self.assertEqual(validate_table(" 20 "), 20)

    def test_validation_rejects_invalid_tables(self) -> None:
        """Verify rejection of tables <= 0, > 20, or non-numeric values."""
        for invalid_table in (0, -1, 21, 99, "table_1", ""):
            with self.assertRaises(ValueError):
                validate_table(invalid_table)

    def test_validation_rejects_unlisted_items(self) -> None:
        """Verify rejection of menu items not present in the catalog."""
        for invalid_item in ("pasta", "sandwich", "tea", "0", "4", "99"):
            with self.assertRaises(ValueError):
                validate_item(invalid_item)

    def test_validation_rejects_invalid_quantities(self) -> None:
        """Verify rejection of non-positive, zero, fractional, or non-numeric quantities."""
        for invalid_qty in (0, -1, -10, "abc", "1.5", ""):
            with self.assertRaises(ValueError):
                validate_quantity(invalid_qty)

    def test_table_clear_and_reset_lifecycle(self) -> None:
        """Verify table orders are completely purged upon bill settlement."""
        add_order(2, "Burger", 1)
        self.assertEqual(len(get_running_order(2)), 1)

        reset_table(2)
        self.assertEqual(len(get_running_order(2)), 0)
        self.assertEqual(format_running_order(2), "Table 2 has no active orders.")


if __name__ == "__main__":
    unittest.main()
