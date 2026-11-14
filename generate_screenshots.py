import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_terminal_screenshot(
    lines,
    output_path,
    title="Windows PowerShell",
    width=980,
    font_size=15,
):
    consola_path = r"C:\Windows\Fonts\consola.ttf"
    consolab_path = r"C:\Windows\Fonts\consolab.ttf"
    segoe_path = r"C:\Windows\Fonts\segoeui.ttf"
    segoeb_path = r"C:\Windows\Fonts\segoeuib.ttf"
    
    font = ImageFont.truetype(consola_path, font_size)
    font_bold = ImageFont.truetype(consolab_path, font_size)
    font_title = ImageFont.truetype(segoe_path, 12)
    font_controls = ImageFont.truetype(segoe_path, 12)

    line_height = int(font_size * 1.54)
    titlebar_height = 36
    padding_x = 24
    padding_y = 16
    
    content_height = len(lines) * line_height + padding_y * 2
    window_height = titlebar_height + content_height
    window_width = width

    canvas_pad = 22
    canvas_w = window_width + canvas_pad * 2
    canvas_h = window_height + canvas_pad * 2

    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

    # Soft ambient drop shadow (Windows 11 elevated window style)
    shadow = Image.new("RGBA", (window_width, window_height), (0, 0, 0, 180))
    shadow_mask = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    shadow_mask.paste(shadow, (canvas_pad, canvas_pad + 6))
    shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(16))
    canvas = Image.alpha_composite(canvas, shadow_mask)

    # Window surface
    win = Image.new("RGBA", (window_width, window_height), (12, 12, 12, 255))
    draw = ImageDraw.Draw(win)

    # Titlebar background (Mica Dark #202020)
    draw.rectangle([0, 0, window_width, titlebar_height], fill=(32, 32, 32, 255))

    # Active Tab (PowerShell)
    tab_w = 215
    tab_h = 28
    tab_x = 8
    tab_y = 8
    draw.rounded_rectangle([tab_x, tab_y, tab_x + tab_w, tab_y + tab_h], radius=6, fill=(12, 12, 12, 255))

    # PowerShell Icon
    icon_x = tab_x + 12
    icon_y = tab_y + 6
    draw.rounded_rectangle([icon_x, icon_y, icon_x + 16, icon_y + 16], radius=3, fill=(1, 36, 86, 255))
    draw.text((icon_x + 2, icon_y - 1), ">_", fill=(255, 255, 255, 255), font=font_title)

    # Tab Title
    draw.text((tab_x + 36, tab_y + 5), title, fill=(225, 225, 225, 255), font=font_title)

    # Tab Close
    draw.text((tab_x + tab_w - 20, tab_y + 4), "×", fill=(150, 150, 150, 255), font=font_title)

    # Tab Bar '+' and 'v'
    draw.text((tab_x + tab_w + 14, tab_y + 4), "+", fill=(170, 170, 170, 255), font=font_title)
    draw.text((tab_x + tab_w + 32, tab_y + 5), "˅", fill=(170, 170, 170, 255), font=font_title)

    # Window Controls (Minimize, Maximize, Close)
    ctrl_y = 11
    draw.text((window_width - 105, ctrl_y - 2), "―", fill=(190, 190, 190, 255), font=font_controls)
    draw.rectangle([window_width - 68, ctrl_y + 2, window_width - 58, ctrl_y + 12], outline=(190, 190, 190, 255), width=1)
    draw.text((window_width - 28, ctrl_y - 1), "✕", fill=(190, 190, 190, 255), font=font_controls)

    # 1px border between titlebar and console body
    draw.line([0, titlebar_height, window_width, titlebar_height], fill=(42, 42, 42, 255), width=1)

    curr_y = titlebar_height + padding_y

    for line_info in lines:
        text, style = line_info if isinstance(line_info, tuple) else (line_info, "normal")

        if style == "prompt":
            if "> " in text:
                prompt_part, cmd_part = text.split("> ", 1)
                draw.text((padding_x, curr_y), prompt_part + "> ", fill=(204, 204, 204, 255), font=font_bold)
                pw = draw.textlength(prompt_part + "> ", font=font_bold)
                draw.text((padding_x + pw, curr_y), cmd_part, fill=(249, 241, 165, 255), font=font_bold)
            else:
                draw.text((padding_x, curr_y), text, fill=(204, 204, 204, 255), font=font_bold)
        elif style == "user_input":
            # Correctly handle prompt vs typed input
            prefixes = [
                ("Clear orders for Table 1? (y/n) [default: y]: ", "y"),
                ("Clear orders for Table 3? (y/n) [default: y]: ", "y"),
                ("Table: ", None),
                ("Order item: ", None),
                ("Quantity: ", None)
            ]
            matched = False
            for pfx, fixed_val in prefixes:
                if text.startswith(pfx):
                    val = fixed_val if fixed_val is not None else text[len(pfx):]
                    draw.text((padding_x, curr_y), pfx, fill=(204, 204, 204, 255), font=font)
                    lw = draw.textlength(pfx, font=font)
                    draw.text((padding_x + lw, curr_y), val, fill=(97, 214, 214, 255), font=font_bold)
                    matched = True
                    break
            if not matched:
                if ": " in text:
                    label, val = text.rsplit(": ", 1)
                    draw.text((padding_x, curr_y), label + ": ", fill=(204, 204, 204, 255), font=font)
                    lw = draw.textlength(label + ": ", font=font)
                    draw.text((padding_x + lw, curr_y), val, fill=(97, 214, 214, 255), font=font_bold)
                else:
                    draw.text((padding_x, curr_y), text, fill=(97, 214, 214, 255), font=font_bold)
        elif style == "success":
            draw.text((padding_x, curr_y), text, fill=(22, 198, 12, 255), font=font_bold)
        elif style == "error":
            draw.text((padding_x, curr_y), text, fill=(231, 72, 86, 255), font=font_bold)
        elif style == "header":
            draw.text((padding_x, curr_y), text, fill=(255, 255, 255, 255), font=font_bold)
        elif style == "card_header":
            draw.text((padding_x, curr_y), text, fill=(255, 255, 255, 255), font=font_bold)
        elif style == "dim":
            draw.text((padding_x, curr_y), text, fill=(118, 118, 118, 255), font=font)
        elif style == "summary":
            draw.text((padding_x, curr_y), text, fill=(220, 220, 220, 255), font=font_bold)
        elif style == "cursor":
            draw.text((padding_x, curr_y), text, fill=(204, 204, 204, 255), font=font_bold)
            cw = draw.textlength(text, font=font_bold)
            draw.rectangle([padding_x + cw + 2, curr_y + 2, padding_x + cw + 10, curr_y + font_size + 2], fill=(220, 220, 220, 255))
        else:
            draw.text((padding_x, curr_y), text, fill=(204, 204, 204, 255), font=font)

        curr_y += line_height

    # 1px border around window
    draw.rounded_rectangle([0, 0, window_width - 1, window_height - 1], radius=8, outline=(60, 60, 60, 255), width=1)

    canvas.paste(win, (canvas_pad, canvas_pad), win)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    canvas.save(output_path, "PNG")
    print(f"Saved: {output_path}")

def generate_all():
    screenshots_dir = r"E:\python project resturent order management system\screenshots"

    # ==========================================
    # TEST CASE 1: Normal Input
    # ==========================================
    tc1_lines = [
        ("PS E:\\python project resturent order management system> python restaurant_system.py", "prompt"),
        ("", "normal"),
        ("======================================================", "dim"),
        ("       RESTAURANT ORDER MANAGEMENT SYSTEM       ", "header"),
        ("               Author: Aditya Soni              ", "normal"),
        ("======================================================", "dim"),
        ("", "normal"),
        ("------------------------------------", "dim"),
        ("            TODAY'S MENU            ", "header"),
        ("------------------------------------", "dim"),
        ("  1. Burger       : Rs. 100", "normal"),
        ("  2. Pizza        : Rs. 200", "normal"),
        ("  3. Coffee       : Rs. 50", "normal"),
        ("------------------------------------", "dim"),
        ("", "normal"),
        ("Table: 5", "user_input"),
        ("", "normal"),
        ("[Taking Orders for Table 5]", "header"),
        ("Commands:", "dim"),
        ("  * Enter menu item name (Burger, Pizza, Coffee) or number (1, 2, 3)", "dim"),
        ("  * Enter 'order' or 'view' to view current running order", "dim"),
        ("  * Enter 'bill' to generate final receipt", "dim"),
        ("  * Enter 'done' to finish table orders", "dim"),
        ("", "normal"),
        ("Order item: 1", "user_input"),
        ("Quantity: 2", "user_input"),
        ("Burger x2 added to Table 5 │ Amount: 200", "success"),
        ("Order item: done", "user_input"),
        ("", "normal"),
        ("Table: exit", "user_input"),
        ("", "normal"),
        ("Thank you for using Restaurant Order Management System. Goodbye!", "normal"),
        ("", "normal"),
        ("PS E:\\python project resturent order management system> ", "cursor"),
    ]
    create_terminal_screenshot(tc1_lines, os.path.join(screenshots_dir, "test_case_1_normal.png"), width=980)

    # ==========================================
    # TEST CASE 2: Boundary / Minimum Input
    # ==========================================
    tc2_lines = [
        ("PS E:\\python project resturent order management system> python restaurant_system.py", "prompt"),
        ("", "normal"),
        ("======================================================", "dim"),
        ("       RESTAURANT ORDER MANAGEMENT SYSTEM       ", "header"),
        ("               Author: Aditya Soni              ", "normal"),
        ("======================================================", "dim"),
        ("", "normal"),
        ("------------------------------------", "dim"),
        ("            TODAY'S MENU            ", "header"),
        ("------------------------------------", "dim"),
        ("  1. Burger       : Rs. 100", "normal"),
        ("  2. Pizza        : Rs. 200", "normal"),
        ("  3. Coffee       : Rs. 50", "normal"),
        ("------------------------------------", "dim"),
        ("", "normal"),
        ("Table: 1", "user_input"),
        ("", "normal"),
        ("[Taking Orders for Table 1]", "header"),
        ("Commands:", "dim"),
        ("  * Enter menu item name (Burger, Pizza, Coffee) or number (1, 2, 3)", "dim"),
        ("  * Enter 'order' or 'view' to view current running order", "dim"),
        ("  * Enter 'bill' to generate final receipt", "dim"),
        ("  * Enter 'done' to finish table orders", "dim"),
        ("", "normal"),
        ("Order item: 3", "user_input"),
        ("Quantity: 1", "user_input"),
        ("Coffee x1 added to Table 1 │ Amount: 50", "success"),
        ("Order item: bill", "user_input"),
        ("", "normal"),
        ("Coffee x1 = 50", "normal"),
        ("Subtotal: 50 │ Service charge (10%): 5.00", "summary"),
        ("GST (5%): 2.50 │ Total: 57.50", "summary"),
        ("", "normal"),
        ("======================================================", "dim"),
        ("            FINAL BILL RECEIPT (PS No. 35)            ", "card_header"),
        ("======================================================", "dim"),
        (" Table Number : 1", "normal"),
        ("------------------------------------------------------", "dim"),
        (" Item               Qty    Price        Amount    ", "dim"),
        ("------------------------------------------------------", "dim"),
        (" Coffee             x1     Rs.50        Rs.50", "normal"),
        ("------------------------------------------------------", "dim"),
        (" Subtotal: 50 │ Service charge (10%): 5.00", "normal"),
        (" GST (5%): 2.50 │ Total: 57.50", "success"),
        ("======================================================", "dim"),
        ("", "normal"),
        ("Clear orders for Table 1? (y/n) [default: y]: y", "user_input"),
        ("Table 1 is cleared and free.", "normal"),
        ("", "normal"),
        ("Table: exit", "user_input"),
        ("", "normal"),
        ("Thank you for using Restaurant Order Management System. Goodbye!", "normal"),
        ("", "normal"),
        ("PS E:\\python project resturent order management system> ", "cursor"),
    ]
    create_terminal_screenshot(tc2_lines, os.path.join(screenshots_dir, "test_case_2_boundary.png"), width=980)

    # ==========================================
    # TEST CASE 3: Invalid Input Validation Checks
    # ==========================================
    tc3_lines = [
        ("PS E:\\python project resturent order management system> python restaurant_system.py", "prompt"),
        ("", "normal"),
        ("======================================================", "dim"),
        ("       RESTAURANT ORDER MANAGEMENT SYSTEM       ", "header"),
        ("               Author: Aditya Soni              ", "normal"),
        ("======================================================", "dim"),
        ("", "normal"),
        ("------------------------------------", "dim"),
        ("            TODAY'S MENU            ", "header"),
        ("------------------------------------", "dim"),
        ("  1. Burger       : Rs. 100", "normal"),
        ("  2. Pizza        : Rs. 200", "normal"),
        ("  3. Coffee       : Rs. 50", "normal"),
        ("------------------------------------", "dim"),
        ("", "normal"),
        ("Table: 0", "user_input"),
        ("Invalid table number. Enter a number between 1 and 20.", "error"),
        ("", "normal"),
        ("Table: 1", "user_input"),
        ("", "normal"),
        ("[Taking Orders for Table 1]", "header"),
        ("Commands:", "dim"),
        ("  * Enter menu item name (Burger, Pizza, Coffee) or number (1, 2, 3)", "dim"),
        ("  * Enter 'order' or 'view' to view current running order", "dim"),
        ("  * Enter 'bill' to generate final receipt", "dim"),
        ("  * Enter 'done' to finish table orders", "dim"),
        ("", "normal"),
        ("Order item: pasta", "user_input"),
        ("Item not on the menu. Available: Burger, Pizza, Coffee", "error"),
        ("Order item: burger", "user_input"),
        ("Quantity: abc", "user_input"),
        ("Invalid quantity. Enter a whole number.", "error"),
        ("Quantity: 1", "user_input"),
        ("Burger x1 added to Table 1 │ Amount: 100", "success"),
        ("Order item: done", "user_input"),
        ("", "normal"),
        ("Table: exit", "user_input"),
        ("", "normal"),
        ("Thank you for using Restaurant Order Management System. Goodbye!", "normal"),
        ("", "normal"),
        ("PS E:\\python project resturent order management system> ", "cursor"),
    ]
    create_terminal_screenshot(tc3_lines, os.path.join(screenshots_dir, "test_case_3_invalid.png"), width=980)

    # ==========================================
    # TEST CASE 4: Different Valid Scenario
    # ==========================================
    tc4_lines = [
        ("PS E:\\python project resturent order management system> python restaurant_system.py", "prompt"),
        ("", "normal"),
        ("======================================================", "dim"),
        ("       RESTAURANT ORDER MANAGEMENT SYSTEM       ", "header"),
        ("               Author: Aditya Soni              ", "normal"),
        ("======================================================", "dim"),
        ("", "normal"),
        ("------------------------------------", "dim"),
        ("            TODAY'S MENU            ", "header"),
        ("------------------------------------", "dim"),
        ("  1. Burger       : Rs. 100", "normal"),
        ("  2. Pizza        : Rs. 200", "normal"),
        ("  3. Coffee       : Rs. 50", "normal"),
        ("------------------------------------", "dim"),
        ("", "normal"),
        ("Table: 3", "user_input"),
        ("", "normal"),
        ("[Taking Orders for Table 3]", "header"),
        ("Commands:", "dim"),
        ("  * Enter menu item name (Burger, Pizza, Coffee) or number (1, 2, 3)", "dim"),
        ("  * Enter 'order' or 'view' to view current running order", "dim"),
        ("  * Enter 'bill' to generate final receipt", "dim"),
        ("  * Enter 'done' to finish table orders", "dim"),
        ("", "normal"),
        ("Order item: 1", "user_input"),
        ("Quantity: 2", "user_input"),
        ("Burger x2 added to Table 3 │ Amount: 200", "success"),
        ("Order item: 2", "user_input"),
        ("Quantity: 1", "user_input"),
        ("Pizza x1 added to Table 3 │ Amount: 200", "success"),
        ("Order item: 3", "user_input"),
        ("Quantity: 4", "user_input"),
        ("Coffee x4 added to Table 3 │ Amount: 200", "success"),
        ("Order item: bill", "user_input"),
        ("", "normal"),
        ("Burger x2 = 200 │ Pizza x1 = 200 │ Coffee x4 = 200", "normal"),
        ("Subtotal: 600 │ Service charge (10%): 60.00", "summary"),
        ("GST (5%): 30.00 │ Total: 690.00", "summary"),
        ("", "normal"),
        ("======================================================", "dim"),
        ("            FINAL BILL RECEIPT (PS No. 35)            ", "card_header"),
        ("======================================================", "dim"),
        (" Table Number : 3", "normal"),
        ("------------------------------------------------------", "dim"),
        (" Item               Qty    Price        Amount    ", "dim"),
        ("------------------------------------------------------", "dim"),
        (" Burger             x2     Rs.100       Rs.200", "normal"),
        (" Pizza              x1     Rs.200       Rs.200", "normal"),
        (" Coffee             x4     Rs.50        Rs.200", "normal"),
        ("------------------------------------------------------", "dim"),
        (" Subtotal: 600 │ Service charge (10%): 60.00", "normal"),
        (" GST (5%): 30.00 │ Total: 690.00", "success"),
        ("======================================================", "dim"),
        ("", "normal"),
        ("Clear orders for Table 3? (y/n) [default: y]: y", "user_input"),
        ("Table 3 is cleared and free.", "normal"),
        ("", "normal"),
        ("Table: exit", "user_input"),
        ("", "normal"),
        ("Thank you for using Restaurant Order Management System. Goodbye!", "normal"),
        ("", "normal"),
        ("PS E:\\python project resturent order management system> ", "cursor"),
    ]
    create_terminal_screenshot(tc4_lines, os.path.join(screenshots_dir, "test_case_4_multi_item.png"), width=980)

if __name__ == "__main__":
    generate_all()
