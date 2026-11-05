"""
=============================================================================
Restaurant Order Management System - Web Frontend Dashboard
Problem Statement No: 35 | B.Tech CSE
Language: Python 3 + Flask
=============================================================================
"""

import sys
import os

# Ensure local imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, request, render_template_string
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
    run_test_case_1,
    run_test_case_2,
    run_test_case_3,
    run_test_case_4,
)

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Restaurant Order Management System | PS No. 35</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0a0e17;
            --bg-secondary: #121826;
            --bg-card: #182234;
            --bg-card-hover: #1f2c42;
            --accent: #f59e0b;
            --accent-glow: rgba(245, 158, 11, 0.25);
            --success: #10b981;
            --danger: #ef4444;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: rgba(255, 255, 255, 0.08);
            --border-active: rgba(245, 158, 11, 0.5);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        body {
            background-color: var(--bg-primary);
            color: var(--text-main);
            min-height: 100vh;
            padding: 24px;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 24px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 28px;
        }

        .header-title h1 {
            font-size: 26px;
            font-weight: 800;
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .badge-ps {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: #000;
            font-size: 12px;
            font-weight: 800;
            padding: 4px 10px;
            border-radius: 6px;
            text-transform: uppercase;
        }

        .header-sub {
            color: var(--text-muted);
            font-size: 14px;
            margin-top: 4px;
        }

        .header-actions {
            display: flex;
            gap: 12px;
        }

        .btn {
            padding: 10px 18px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            border: 1px solid transparent;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .btn-primary {
            background: #f59e0b;
            color: #000;
        }
        .btn-primary:hover {
            background: #d97706;
            box-shadow: 0 4px 14px var(--accent-glow);
        }

        .btn-secondary {
            background: var(--bg-secondary);
            color: var(--text-main);
            border-color: var(--border);
        }
        .btn-secondary:hover {
            background: var(--bg-card);
            border-color: var(--accent);
        }

        .btn-success {
            background: #10b981;
            color: #fff;
        }
        .btn-success:hover {
            background: #059669;
        }

        .layout-grid {
            display: grid;
            grid-template-columns: 340px 1fr 380px;
            gap: 24px;
        }

        .panel {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 18px;
        }

        .panel-header {
            font-size: 16px;
            font-weight: 700;
            color: var(--text-main);
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border);
        }

        /* Tables Grid */
        .tables-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            max-height: 440px;
            overflow-y: auto;
            padding-right: 4px;
        }

        .table-chip {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 14px 8px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
        }

        .table-chip:hover {
            background: var(--bg-card-hover);
            transform: translateY(-2px);
        }

        .table-chip.selected {
            border-color: var(--accent);
            background: rgba(245, 158, 11, 0.15);
            box-shadow: 0 0 16px var(--accent-glow);
        }

        .table-chip.occupied {
            border-color: var(--success);
        }

        .table-chip .tbl-num {
            font-size: 15px;
            font-weight: 700;
        }

        .table-chip .tbl-status {
            font-size: 11px;
            color: var(--text-muted);
            margin-top: 4px;
        }

        .table-chip.occupied .tbl-status {
            color: var(--success);
            font-weight: 600;
        }

        /* Menu Items */
        .menu-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
        }

        .menu-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            transition: all 0.2s;
        }

        .menu-card:hover {
            border-color: var(--accent);
            background: var(--bg-card-hover);
        }

        .menu-icon {
            font-size: 32px;
        }

        .menu-name {
            font-size: 18px;
            font-weight: 700;
        }

        .menu-price {
            font-size: 16px;
            font-weight: 800;
            color: var(--accent);
            font-family: 'JetBrains Mono', monospace;
        }

        .qty-controls {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 8px;
        }

        .qty-input {
            width: 60px;
            padding: 8px;
            border-radius: 6px;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            color: #fff;
            text-align: center;
            font-weight: 600;
        }

        /* Order Bill Panel */
        .order-items-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
            max-height: 240px;
            overflow-y: auto;
        }

        .order-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 12px;
            background: var(--bg-card);
            border-radius: 8px;
            font-size: 13px;
        }

        .bill-calc-box {
            background: var(--bg-primary);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
        }

        .calc-row {
            display: flex;
            justify-content: space-between;
            color: var(--text-muted);
        }

        .calc-row.total {
            color: var(--accent);
            font-size: 16px;
            font-weight: 800;
            border-top: 1px dashed var(--border);
            padding-top: 8px;
            margin-top: 4px;
        }

        /* Test Suite Box */
        .test-suite-box {
            background: #06090e;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            margin-top: 24px;
        }

        .test-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
        }

        .test-buttons {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .test-btn {
            padding: 8px 14px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            color: #fff;
        }
        .test-btn:hover {
            border-color: var(--accent);
            color: var(--accent);
        }

        .console-output {
            background: #020408;
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 14px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            color: #10b981;
            white-space: pre-wrap;
            max-height: 200px;
            overflow-y: auto;
            margin-top: 12px;
        }

        .toast {
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: #fff;
            padding: 14px 20px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            display: none;
            z-index: 1000;
        }
    </style>
</head>
<body>

    <header class="header">
        <div class="header-title">
            <h1>
                🍽️ Restaurant Order Management System
                <span class="badge-ps">PS No. 35</span>
            </h1>
            <p class="header-sub">B.Tech Computer Science and Engineering | Python 3 + Console + Web POS</p>
        </div>
        <div class="header-actions">
            <button class="btn btn-secondary" onclick="runAutomatedTests()">⚡ Run All 4 Test Cases</button>
            <button class="btn btn-primary" onclick="generateBill()">🧾 Generate Bill</button>
        </div>
    </header>

    <div class="layout-grid">
        <!-- Panel 1: Table Selector -->
        <div class="panel">
            <div class="panel-header">
                <span>🪑 Table Selection (1 - 20)</span>
                <span id="selected-table-label" style="color: var(--accent);">Table 1</span>
            </div>
            <div class="tables-grid" id="tables-container">
                <!-- Dynamically generated 20 tables -->
            </div>
        </div>

        <!-- Panel 2: Menu Items -->
        <div class="panel">
            <div class="panel-header">
                <span>📋 Restaurant Menu (Dictionary)</span>
                <span style="font-size: 13px; color: var(--text-muted);">10% Svc + 5% GST</span>
            </div>

            <div class="menu-grid">
                <div class="menu-card">
                    <div class="menu-icon">🍔</div>
                    <div class="menu-name">Burger</div>
                    <div class="menu-price">Rs. 100</div>
                    <div class="qty-controls">
                        <input type="number" id="qty-Burger" class="qty-input" value="1" min="1">
                        <button class="btn btn-primary" style="flex:1;" onclick="addItem('Burger')">+ Add</button>
                    </div>
                </div>

                <div class="menu-card">
                    <div class="menu-icon">🍕</div>
                    <div class="menu-name">Pizza</div>
                    <div class="menu-price">Rs. 200</div>
                    <div class="qty-controls">
                        <input type="number" id="qty-Pizza" class="qty-input" value="1" min="1">
                        <button class="btn btn-primary" style="flex:1;" onclick="addItem('Pizza')">+ Add</button>
                    </div>
                </div>

                <div class="menu-card">
                    <div class="menu-icon">☕</div>
                    <div class="menu-name">Coffee</div>
                    <div class="menu-price">Rs. 50</div>
                    <div class="qty-controls">
                        <input type="number" id="qty-Coffee" class="qty-input" value="1" min="1">
                        <button class="btn btn-primary" style="flex:1;" onclick="addItem('Coffee')">+ Add</button>
                    </div>
                </div>
            </div>

            <!-- Running Order Display -->
            <div style="margin-top: 10px;">
                <h4 style="font-size: 14px; margin-bottom: 8px;">Active Running Order:</h4>
                <div id="running-order-summary" style="font-family: 'JetBrains Mono', monospace; font-size: 13px; padding: 12px; background: var(--bg-primary); border-radius: 8px; border: 1px solid var(--border); color: #cbd5e1;">
                    Table 1 has no active orders.
                </div>
            </div>
        </div>

        <!-- Panel 3: Live Order Bill & Checkout -->
        <div class="panel">
            <div class="panel-header">
                <span>🧾 Table Bill & Summary</span>
                <button class="btn btn-secondary" style="padding: 4px 10px; font-size: 12px;" onclick="clearTable()">Clear</button>
            </div>

            <div class="order-items-list" id="order-items-container">
                <!-- Dynamically rendered order items -->
            </div>

            <div class="bill-calc-box">
                <div class="calc-row">
                    <span>Subtotal:</span>
                    <span id="bill-subtotal">Rs. 0</span>
                </div>
                <div class="calc-row">
                    <span>Service Charge (10%):</span>
                    <span id="bill-service">Rs. 0.00</span>
                </div>
                <div class="calc-row">
                    <span>GST (5%):</span>
                    <span id="bill-gst">Rs. 0.00</span>
                </div>
                <div class="calc-row total">
                    <span>Total Payable:</span>
                    <span id="bill-total">Rs. 0.00</span>
                </div>
            </div>

            <button class="btn btn-success" style="width: 100%; justify-content: center; padding: 12px;" onclick="generateBill()">
                ✓ Print / Finalize Bill
            </button>
        </div>
    </div>

    <!-- Test Suite Console -->
    <div class="test-suite-box">
        <div class="test-header">
            <span style="font-weight: 700; font-size: 15px;">🧪 Interactive Academic Verification Suite (PS No. 35)</span>
            <div class="test-buttons">
                <button class="test-btn" onclick="runSingleTest(1)">Test Case 1 (Normal)</button>
                <button class="test-btn" onclick="runSingleTest(2)">Test Case 2 (Boundary)</button>
                <button class="test-btn" onclick="runSingleTest(3)">Test Case 3 (Invalid)</button>
                <button class="test-btn" onclick="runSingleTest(4)">Test Case 4 (Multi-item)</button>
                <button class="test-btn" style="background: #f59e0b; color: #000;" onclick="runAutomatedTests()">Run All</button>
            </div>
        </div>
        <div class="console-output" id="console-output">Output console ready. Click any test case above to run verification.</div>
    </div>

    <div class="toast" id="toast">Order added successfully!</div>

    <script>
        let currentTable = 1;

        function showToast(msg) {
            const t = document.getElementById("toast");
            t.innerText = msg;
            t.style.display = "block";
            setTimeout(() => { t.style.display = "none"; }, 2500);
        }

        async function fetchTables() {
            const res = await fetch("/api/tables");
            const data = await res.json();
            const container = document.getElementById("tables-container");
            container.innerHTML = "";

            for (let i = 1; i <= 20; i++) {
                const isOccupied = data[i] && data[i].length > 0;
                const isSelected = (i === currentTable);
                const chip = document.createElement("div");
                chip.className = `table-chip ${isSelected ? 'selected' : ''} ${isOccupied ? 'occupied' : ''}`;
                chip.onclick = () => selectTable(i);
                chip.innerHTML = `
                    <div class="tbl-num">T-${i}</div>
                    <div class="tbl-status">${isOccupied ? data[i].length + ' items' : 'Empty'}</div>
                `;
                container.appendChild(chip);
            }
            fetchTableDetails(currentTable);
        }

        function selectTable(tbl) {
            currentTable = tbl;
            document.getElementById("selected-table-label").innerText = "Table " + tbl;
            fetchTables();
        }

        async function fetchTableDetails(tbl) {
            const res = await fetch(`/api/table/${tbl}`);
            const data = await res.json();

            // Render order items
            const container = document.getElementById("order-items-container");
            container.innerHTML = "";

            if (!data.orders || data.orders.length === 0) {
                container.innerHTML = `<div style="color: var(--text-muted); font-size: 13px; text-align: center; padding: 20px;">No items ordered yet.</div>`;
            } else {
                data.orders.forEach(o => {
                    const row = document.createElement("div");
                    row.className = "order-row";
                    row.innerHTML = `
                        <div>
                            <strong>${o.item}</strong> x${o.quantity}
                            <div style="font-size: 11px; color: var(--text-muted);">Rs. ${o.price} each</div>
                        </div>
                        <div style="font-weight: 700; color: var(--accent);">Rs. ${o.amount}</div>
                    `;
                    container.appendChild(row);
                });
            }

            // Running summary
            document.getElementById("running-order-summary").innerText = data.running_order || `Table ${tbl} has no active orders.`;

            // Bill Breakdown
            document.getElementById("bill-subtotal").innerText = "Rs. " + data.bill.subtotal;
            document.getElementById("bill-service").innerText = "Rs. " + Number(data.bill.service_charge).toFixed(2);
            document.getElementById("bill-gst").innerText = "Rs. " + Number(data.bill.gst).toFixed(2);
            document.getElementById("bill-total").innerText = "Rs. " + Number(data.bill.total).toFixed(2);
        }

        async function addItem(item) {
            const qty = document.getElementById(`qty-${item}`).value;
            const res = await fetch("/api/order", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({table: currentTable, item: item, quantity: qty})
            });
            const data = await res.json();
            if (data.success) {
                showToast(data.message);
                fetchTables();
            } else {
                alert(data.error);
            }
        }

        async function clearTable() {
            if (!confirm(`Clear all orders for Table ${currentTable}?`)) return;
            const res = await fetch(`/api/table/${currentTable}/clear`, {method: "POST"});
            const data = await res.json();
            showToast(data.message);
            fetchTables();
        }

        async function generateBill() {
            const res = await fetch(`/api/table/${currentTable}`);
            const data = await res.json();
            if (!data.orders || data.orders.length === 0) {
                alert(`Table ${currentTable} has no active orders!`);
                return;
            }
            alert(`Receipt for Table ${currentTable}:\\n` + data.bill.summary_line);
        }

        async function runSingleTest(testNum) {
            const out = document.getElementById("console-output");
            out.innerText = `Running Test Case ${testNum}...`;
            const res = await fetch(`/api/test/${testNum}`);
            const data = await res.json();
            out.innerText = data.log;
            fetchTables();
        }

        async function runAutomatedTests() {
            const out = document.getElementById("console-output");
            out.innerText = "Executing complete academic verification suite (All 4 cases)...";
            const res = await fetch("/api/test/all");
            const data = await res.json();
            out.innerText = data.log;
            fetchTables();
        }

        window.onload = fetchTables;
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/tables", methods=["GET"])
def api_tables():
    return jsonify(table_orders)

@app.route("/api/table/<int:tbl>", methods=["GET"])
def api_table_details(tbl):
    try:
        t = validate_table(tbl)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    orders = get_running_order(t)
    running_str = format_running_order(t)
    bill = calculate_bill(t)
    return jsonify({
        "table": t,
        "orders": orders,
        "running_order": running_str,
        "bill": bill
    })

@app.route("/api/order", methods=["POST"])
def api_add_order():
    data = request.json or {}
    try:
        t = validate_table(data.get("table"))
        item = validate_item(data.get("item"))
        qty = validate_quantity(data.get("quantity"))
        res = add_order(t, item, qty)
        return jsonify({"success": True, "message": res["message"], "amount": res["amount"]})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/table/<int:tbl>/clear", methods=["POST"])
def api_clear_table(tbl):
    reset_table(tbl)
    return jsonify({"success": True, "message": f"Table {tbl} cleared successfully."})

@app.route("/api/test/<test_id>", methods=["GET"])
def api_run_test(test_id):
    import io
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        if test_id == "1":
            run_test_case_1()
        elif test_id == "2":
            run_test_case_2()
        elif test_id == "3":
            run_test_case_3()
        elif test_id == "4":
            run_test_case_4()
        elif test_id == "all":
            from restaurant_system import run_all_tests_auto
            run_all_tests_auto()
        else:
            print(f"Invalid test ID: {test_id}")

    return jsonify({"log": buf.getvalue()})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n==================================================")
    print(f" RESTAURANT ORDER MANAGEMENT SYSTEM - WEB DASHBOARD")
    print(f" Running at: http://127.0.0.1:{port}")
    print(f"==================================================\n")
    app.run(host="0.0.0.0", port=port, debug=False)
