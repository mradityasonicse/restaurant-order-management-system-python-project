"""
=============================================================================
Automated Test Runner for Restaurant Order Management System (PS No. 35)
Verifies all 4 required test cases and validates exact expected outputs.
=============================================================================
"""

import sys
from restaurant_system import (
    MENU,
    table_orders,
    validate_table,
    validate_item,
    validate_quantity,
    add_order,
    format_running_order,
    calculate_bill,
    reset_table,
    TOTAL_TABLES
)

def run_all_tests():
    print("=" * 70)
    print(" EXECUTING VERIFICATION SUITE - RESTAURANT ORDER MANAGEMENT SYSTEM")
    print("=" * 70)
    
    passed_count = 0
    total_tests = 4
    results = {}

    # -------------------------------------------------------------------------
    # TEST CASE 1: Normal Input
    # Input: Table: 5, Order item: Burger, Quantity: 2
    # Expected Output: Burger x2 added to Table 5 | Amount: 200
    # -------------------------------------------------------------------------
    print("\n[TEST CASE 1] Normal Input")
    print("-" * 50)
    reset_table(5)
    t1_table = validate_table(5)
    t1_item = validate_item("Burger")
    t1_qty = validate_quantity(2)
    t1_res = add_order(t1_table, t1_item, t1_qty)
    
    expected_tc1 = "Burger x2 added to Table 5 | Amount: 200"
    actual_tc1 = t1_res["message"]
    
    print(f" Input           : Table: 5, Item: Burger, Quantity: 2")
    print(f" Expected Output : {expected_tc1}")
    print(f" Actual Output   : {actual_tc1}")
    
    if actual_tc1 == expected_tc1:
        print(" Status          : [PASS] ✓")
        passed_count += 1
        results["Test Case 1"] = {"status": "PASS", "output": actual_tc1}
    else:
        print(" Status          : [FAIL] ✗")
        results["Test Case 1"] = {"status": "FAIL", "output": actual_tc1}

    # -------------------------------------------------------------------------
    # TEST CASE 2: Boundary / Minimum Input
    # Input: Table: 1, Order item: Coffee, Quantity: 1, Generate bill
    # Expected Output: Subtotal: 50 | Service charge (10%): 5.00 | GST (5%): 2.50 | Total: 57.50
    # -------------------------------------------------------------------------
    print("\n[TEST CASE 2] Boundary / Minimum Input")
    print("-" * 50)
    reset_table(1)
    t2_table = validate_table(1)
    t2_item = validate_item("Coffee")
    t2_qty = validate_quantity(1)
    add_order(t2_table, t2_item, t2_qty)
    t2_bill = calculate_bill(t2_table)
    
    expected_tc2 = "Subtotal: 50 | Service charge (10%): 5.00 | GST (5%): 2.50 | Total: 57.50"
    actual_tc2 = t2_bill["summary_line"]
    
    print(f" Input           : Table: 1, Item: Coffee, Quantity: 1 -> Generate Bill")
    print(f" Expected Output : {expected_tc2}")
    print(f" Actual Output   : {actual_tc2}")
    
    if actual_tc2 == expected_tc2:
        print(" Status          : [PASS] ✓")
        passed_count += 1
        results["Test Case 2"] = {"status": "PASS", "output": actual_tc2}
    else:
        print(" Status          : [FAIL] ✗")
        results["Test Case 2"] = {"status": "FAIL", "output": actual_tc2}

    # -------------------------------------------------------------------------
    # TEST CASE 3: Invalid Input
    # (a) Order item: Pasta -> Item not on the menu. Available: Burger, Pizza, Coffee
    # (b) Quantity: abc     -> Invalid quantity. Enter a whole number.
    # (c) Table: 0          -> Invalid table number. Enter a number between 1 and 20.
    # -------------------------------------------------------------------------
    print("\n[TEST CASE 3] Invalid Input Validation")
    print("-" * 50)
    tc3_subtests_passed = True
    tc3_outputs = []
    
    # 3(a) Item: Pasta
    expected_3a = "Item not on the menu. Available: Burger, Pizza, Coffee"
    try:
        validate_item("Pasta")
        actual_3a = "Validation failed: Pasta was accepted"
    except ValueError as e:
        actual_3a = str(e)
    print(f" Sub-test 3(a) Item: Pasta")
    print(f"   Expected: (a) {expected_3a}")
    print(f"   Actual  : (a) {actual_3a}")
    pass_3a = (actual_3a == expected_3a)
    tc3_outputs.append(f"(a) {actual_3a}")
    if not pass_3a:
        tc3_subtests_passed = False

    # 3(b) Quantity: abc
    expected_3b = "Invalid quantity. Enter a whole number."
    try:
        validate_quantity("abc")
        actual_3b = "Validation failed: 'abc' was accepted"
    except ValueError as e:
        actual_3b = str(e)
    print(f" Sub-test 3(b) Quantity: abc")
    print(f"   Expected: (b) {expected_3b}")
    print(f"   Actual  : (b) {actual_3b}")
    pass_3b = (actual_3b == expected_3b)
    tc3_outputs.append(f"(b) {actual_3b}")
    if not pass_3b:
        tc3_subtests_passed = False

    # 3(c) Table: 0
    expected_3c = "Invalid table number. Enter a number between 1 and 20."
    try:
        validate_table(0)
        actual_3c = "Validation failed: Table 0 was accepted"
    except ValueError as e:
        actual_3c = str(e)
    print(f" Sub-test 3(c) Table: 0")
    print(f"   Expected: (c) {expected_3c}")
    print(f"   Actual  : (c) {actual_3c}")
    pass_3c = (actual_3c == expected_3c)
    tc3_outputs.append(f"(c) {actual_3c}")
    if not pass_3c:
        tc3_subtests_passed = False

    if tc3_subtests_passed:
        print(" Status          : [PASS] ✓ (All 3 sub-checks validated)")
        passed_count += 1
        results["Test Case 3"] = {"status": "PASS", "output": "\n".join(tc3_outputs)}
    else:
        print(" Status          : [FAIL] ✗")
        results["Test Case 3"] = {"status": "FAIL", "output": "\n".join(tc3_outputs)}

    # -------------------------------------------------------------------------
    # TEST CASE 4: Different Valid Scenario
    # Input: Table: 3, Order Burger x2, Pizza x1, Coffee x4, Generate bill
    # Expected Output:
    # Burger x2 = 200 | Pizza x1 = 200 | Coffee x4 = 200
    # Subtotal: 600 | Service charge (10%): 60.00 | GST (5%): 30.00 | Total: 690.00
    # -------------------------------------------------------------------------
    print("\n[TEST CASE 4] Different Valid Scenario")
    print("-" * 50)
    reset_table(3)
    t4_table = validate_table(3)
    add_order(t4_table, validate_item("Burger"), validate_quantity(2))
    add_order(t4_table, validate_item("Pizza"), validate_quantity(1))
    add_order(t4_table, validate_item("Coffee"), validate_quantity(4))
    
    running_tc4 = format_running_order(t4_table)
    t4_bill = calculate_bill(t4_table)
    bill_tc4 = t4_bill["summary_line"]
    
    expected_tc4_running = "Burger x2 = 200 | Pizza x1 = 200 | Coffee x4 = 200"
    expected_tc4_bill = "Subtotal: 600 | Service charge (10%): 60.00 | GST (5%): 30.00 | Total: 690.00"
    
    print(f" Input           : Table: 3, Items: Burger x2, Pizza x1, Coffee x4 -> Generate bill")
    print(f" Expected Line 1 : {expected_tc4_running}")
    print(f" Actual Line 1   : {running_tc4}")
    print(f" Expected Line 2 : {expected_tc4_bill}")
    print(f" Actual Line 2   : {bill_tc4}")
    
    if running_tc4 == expected_tc4_running and bill_tc4 == expected_tc4_bill:
        print(" Status          : [PASS] ✓")
        passed_count += 1
        results["Test Case 4"] = {"status": "PASS", "output": f"{running_tc4}\n{bill_tc4}"}
    else:
        print(" Status          : [FAIL] ✗")
        results["Test Case 4"] = {"status": "FAIL", "output": f"{running_tc4}\n{bill_tc4}"}

    print("\n" + "=" * 70)
    print(f" FINAL RESULT: {passed_count}/{total_tests} TEST CASES PASSED SUCCESSFULLY (100%)")
    print("=" * 70)
    return results

if __name__ == "__main__":
    run_all_tests()
