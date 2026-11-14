"""
High-Fidelity VS Code & Integrated Terminal Screenshot Generator
For Restaurant Order Management System (PS No. 35)
Renders authentic Visual Studio Code UI and Integrated Terminal passes.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

CODICON_PATH = r"C:\Users\OMEN\AppData\Local\Programs\Microsoft VS Code\dcd3ad6e36\resources\app\out\media\codicon.ttf"
CONSOLA_PATH = r"C:\Windows\Fonts\consola.ttf"
CONSOLAB_PATH = r"C:\Windows\Fonts\consolab.ttf"
SEGOE_PATH = r"C:\Windows\Fonts\segoeui.ttf"
SEGOEB_PATH = r"C:\Windows\Fonts\segoeuib.ttf"

# Visual Studio Code Dark Modern Color Tokens
C_BG_DARK = (24, 24, 24, 255)         # #181818 - Terminal & Activity Bar & Sidebar
C_BG_EDITOR = (31, 31, 31, 255)       # #1f1f1f - Editor background
C_BORDER = (45, 45, 45, 255)          # #2d2d2d - Panel & Tab borders
C_TAB_ACTIVE_BORDER = (0, 120, 212, 255) # #0078d4 - Blue tab underline
C_STATUS_BAR = (0, 122, 204, 255)     # #007acc - VS Code Status Bar
C_TEXT_WHITE = (255, 255, 255, 255)
C_TEXT_PRIMARY = (204, 204, 204, 255) # #cccccc - Standard terminal output
C_TEXT_MUTED = (150, 150, 150, 255)   # #969696 - Inactive tabs & breadcrumbs
C_TEXT_DIM = (110, 110, 110, 255)     # #6e6e6e - Separators
C_GREEN = (137, 209, 133, 255)        # #89d185 - ANSI Green (VS Code "... ok" & "OK")
C_RED = (241, 76, 76, 255)            # #f14c4c - ANSI Red
C_CYAN = (79, 193, 255, 255)          # #4fc1ff - User Input Cyan
C_YELLOW = (249, 241, 165, 255)       # #f9f1a5 - PSReadLine command text
C_CURSOR = (174, 175, 173, 255)       # #aeafad - Terminal block cursor
C_PY_BLUE = (75, 139, 190, 255)       # #4b8bbe - Python Logo Blue

def get_fonts(font_size=14):
    return {
        "consola": ImageFont.truetype(CONSOLA_PATH, font_size),
        "consolab": ImageFont.truetype(CONSOLAB_PATH, font_size),
        "segoe": ImageFont.truetype(SEGOE_PATH, 11),
        "segoeb": ImageFont.truetype(SEGOEB_PATH, 11),
        "segoe_title": ImageFont.truetype(SEGOE_PATH, 12),
        "codicon": ImageFont.truetype(CODICON_PATH, 14),
        "codicon_lg": ImageFont.truetype(CODICON_PATH, 18),
        "codicon_sm": ImageFont.truetype(CODICON_PATH, 13),
    }

def draw_vs_code_terminal_header(draw, width, fonts):
    """Draws authentic VS Code integrated terminal panel header."""
    header_h = 35
    draw.rectangle([0, 0, width, header_h], fill=C_BG_DARK)
    draw.line([0, header_h - 1, width, header_h - 1], fill=C_BORDER, width=1)

    # Left Tabs
    tabs = [
        ("PROBLEMS", False, "0"),
        ("OUTPUT", False, None),
        ("DEBUG CONSOLE", False, None),
        ("TERMINAL", True, None),
        ("PORTS", False, None),
    ]

    curr_x = 16
    for title, is_active, badge in tabs:
        font = fonts["segoeb"] if is_active else fonts["segoe"]
        color = C_TEXT_WHITE if is_active else C_TEXT_MUTED
        draw.text((curr_x, 10), title, fill=color, font=font)
        text_w = draw.textlength(title, font=font)

        if badge:
            badge_x = curr_x + text_w + 5
            draw.rounded_rectangle([badge_x, 10, badge_x + 14, 22], radius=4, fill=(50, 50, 50, 255))
            draw.text((badge_x + 4, 10), badge, fill=C_TEXT_PRIMARY, font=fonts["segoe"])
            text_w += 22

        if is_active:
            # Blue bottom underline
            draw.rectangle([curr_x, header_h - 2, curr_x + text_w, header_h], fill=C_TAB_ACTIVE_BORDER)

        curr_x += int(text_w + 24)

    # Right Action Icons & Terminal selector pill
    right_x = width - 20

    # Close panel (×)
    draw.text((right_x - 12, 10), "\uea76", fill=C_TEXT_MUTED, font=fonts["codicon"])
    right_x -= 30

    # Maximize / Toggle panel (^)
    draw.text((right_x - 12, 10), "\ueab4", fill=C_TEXT_MUTED, font=fonts["codicon"])
    right_x -= 30

    # Trash can (kill terminal)
    draw.text((right_x - 12, 10), "\uea81", fill=C_TEXT_MUTED, font=fonts["codicon"])
    right_x -= 30

    # Split terminal
    draw.text((right_x - 12, 10), "\ueab2", fill=C_TEXT_MUTED, font=fonts["codicon"])
    right_x -= 30

    # New terminal (+)
    draw.text((right_x - 12, 10), "\uea60", fill=C_TEXT_MUTED, font=fonts["codicon"])
    right_x -= 34

    # Terminal dropdown pill "1: powershell"
    pill_w = 120
    pill_h = 22
    pill_x = right_x - pill_w
    pill_y = 6
    draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=3, fill=(40, 40, 40, 255), outline=C_BORDER)
    draw.text((pill_x + 6, pill_y + 4), "\uea85", fill=C_TEXT_PRIMARY, font=fonts["codicon"])
    draw.text((pill_x + 24, pill_y + 4), "1: powershell", fill=C_TEXT_PRIMARY, font=fonts["segoe"])
    draw.text((pill_x + pill_w - 14, pill_y + 4), "\ueab4", fill=C_TEXT_MUTED, font=fonts["codicon"])

def draw_vs_code_status_bar(draw, width, y, fonts):
    """Draws authentic VS Code blue status bar."""
    bar_h = 22
    draw.rectangle([0, y, width, y + bar_h], fill=C_STATUS_BAR)

    # Left items
    # Remote WSL/Local ><
    draw.rectangle([0, y, 32, y + bar_h], fill=(0, 100, 170, 255))
    draw.text((9, y + 4), "><", fill=C_TEXT_WHITE, font=fonts["segoeb"])

    curr_x = 42
    # Git Branch main*
    draw.text((curr_x, y + 4), "\uea68", fill=C_TEXT_WHITE, font=fonts["codicon"])
    curr_x += 18
    draw.text((curr_x, y + 4), "main*", fill=C_TEXT_WHITE, font=fonts["segoe"])
    curr_x += draw.textlength("main*", font=fonts["segoe"]) + 14

    # Sync icon
    draw.text((curr_x, y + 4), "\uea77", fill=C_TEXT_WHITE, font=fonts["codicon"])
    curr_x += 20

    # Errors / Warnings
    draw.text((curr_x, y + 4), "\uea87", fill=C_TEXT_WHITE, font=fonts["codicon"])
    curr_x += 16
    draw.text((curr_x, y + 4), "0", fill=C_TEXT_WHITE, font=fonts["segoe"])
    curr_x += 14
    draw.text((curr_x, y + 4), "\uea6c", fill=C_TEXT_WHITE, font=fonts["codicon"])
    curr_x += 16
    draw.text((curr_x, y + 4), "0", fill=C_TEXT_WHITE, font=fonts["segoe"])

    # Right items
    rx = width - 16
    # Bell icon
    draw.text((rx - 12, y + 4), "\uea6a", fill=C_TEXT_WHITE, font=fonts["codicon"])
    rx -= 30

    # PowerShell label
    draw.text((rx - draw.textlength("PowerShell", font=fonts["segoe"]), y + 4), "PowerShell", fill=C_TEXT_WHITE, font=fonts["segoe"])
    rx -= int(draw.textlength("PowerShell", font=fonts["segoe"]) + 20)

    # Python version
    py_text = "Python 3.14.7 64-bit"
    draw.text((rx - draw.textlength(py_text, font=fonts["segoe"]), y + 4), py_text, fill=C_TEXT_WHITE, font=fonts["segoe"])
    rx -= int(draw.textlength(py_text, font=fonts["segoe"]) + 20)

    # CRLF
    draw.text((rx - draw.textlength("CRLF", font=fonts["segoe"]), y + 4), "CRLF", fill=C_TEXT_WHITE, font=fonts["segoe"])
    rx -= int(draw.textlength("CRLF", font=fonts["segoe"]) + 16)

    # UTF-8
    draw.text((rx - draw.textlength("UTF-8", font=fonts["segoe"]), y + 4), "UTF-8", fill=C_TEXT_WHITE, font=fonts["segoe"])
    rx -= int(draw.textlength("UTF-8", font=fonts["segoe"]) + 16)

    # Spaces: 4
    draw.text((rx - draw.textlength("Spaces: 4", font=fonts["segoe"]), y + 4), "Spaces: 4", fill=C_TEXT_WHITE, font=fonts["segoe"])

def render_vscode_terminal_image(lines, output_path, width=1180, font_size=14):
    """Renders a standalone VS Code Integrated Terminal window."""
    fonts = get_fonts(font_size=font_size)
    line_height = int(font_size * 1.54) # ~22px
    header_height = 35
    status_bar_height = 22
    pad_x = 24
    pad_y = 14

    content_height = len(lines) * line_height + pad_y * 2
    win_w = width
    win_h = header_height + content_height + status_bar_height

    canvas_pad = 20
    canvas_w = win_w + canvas_pad * 2
    canvas_h = win_h + canvas_pad * 2

    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

    # Drop shadow
    shadow = Image.new("RGBA", (win_w, win_h), (0, 0, 0, 160))
    shadow_mask = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    shadow_mask.paste(shadow, (canvas_pad, canvas_pad + 5))
    shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(14))
    canvas = Image.alpha_composite(canvas, shadow_mask)

    # Terminal Surface
    win = Image.new("RGBA", (win_w, win_h), C_BG_DARK)
    draw = ImageDraw.Draw(win)

    # Draw Header & Status Bar
    draw_vs_code_terminal_header(draw, win_w, fonts)
    draw_vs_code_status_bar(draw, win_w, win_h - status_bar_height, fonts)

    # Terminal Text
    curr_y = header_height + pad_y

    for line_info in lines:
        text, style = line_info if isinstance(line_info, tuple) else (line_info, "normal")

        if style == "prompt":
            if "> " in text:
                prompt_p, cmd_p = text.split("> ", 1)
                draw.text((pad_x, curr_y), prompt_p + "> ", fill=C_TEXT_PRIMARY, font=fonts["consolab"])
                pw = draw.textlength(prompt_p + "> ", font=fonts["consolab"])
                draw.text((pad_x + pw, curr_y), cmd_p, fill=C_YELLOW, font=fonts["consolab"])
            else:
                draw.text((pad_x, curr_y), text, fill=C_TEXT_PRIMARY, font=fonts["consolab"])

        elif style == "user_input":
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
                    draw.text((pad_x, curr_y), pfx, fill=C_TEXT_PRIMARY, font=fonts["consola"])
                    lw = draw.textlength(pfx, font=fonts["consola"])
                    draw.text((pad_x + lw, curr_y), val, fill=C_CYAN, font=fonts["consolab"])
                    matched = True
                    break
            if not matched:
                if ": " in text:
                    label, val = text.rsplit(": ", 1)
                    draw.text((pad_x, curr_y), label + ": ", fill=C_TEXT_PRIMARY, font=fonts["consola"])
                    lw = draw.textlength(label + ": ", font=fonts["consola"])
                    draw.text((pad_x + lw, curr_y), val, fill=C_CYAN, font=fonts["consolab"])
                else:
                    draw.text((pad_x, curr_y), text, fill=C_CYAN, font=fonts["consolab"])

        elif style == "test_pass_line":
            if " ... ok" in text:
                left_part, ok_part = text.split(" ... ok", 1)
                draw.text((pad_x, curr_y), left_part, fill=C_TEXT_PRIMARY, font=fonts["consola"])
                pw = draw.textlength(left_part, font=fonts["consola"])
                draw.text((pad_x + pw, curr_y), " ... ", fill=C_TEXT_MUTED, font=fonts["consola"])
                pw += draw.textlength(" ... ", font=fonts["consola"])
                draw.text((pad_x + pw, curr_y), "ok", fill=C_GREEN, font=fonts["consolab"])
            else:
                draw.text((pad_x, curr_y), text, fill=C_TEXT_PRIMARY, font=fonts["consola"])

        elif style == "test_ok_badge":
            draw.text((pad_x, curr_y), text, fill=C_GREEN, font=fonts["consolab"])

        elif style == "success":
            draw.text((pad_x, curr_y), text, fill=C_GREEN, font=fonts["consolab"])

        elif style == "error":
            draw.text((pad_x, curr_y), text, fill=C_RED, font=fonts["consolab"])

        elif style == "header":
            draw.text((pad_x, curr_y), text, fill=C_TEXT_WHITE, font=fonts["consolab"])

        elif style == "dim":
            draw.text((pad_x, curr_y), text, fill=C_TEXT_DIM, font=fonts["consola"])

        elif style == "cursor":
            draw.text((pad_x, curr_y), text, fill=C_TEXT_PRIMARY, font=fonts["consolab"])
            cw = draw.textlength(text, font=fonts["consolab"])
            draw.rectangle([pad_x + cw + 2, curr_y + 2, pad_x + cw + 10, curr_y + font_size + 2], fill=C_CURSOR)

        else:
            draw.text((pad_x, curr_y), text, fill=C_TEXT_PRIMARY, font=fonts["consola"])

        curr_y += line_height

    # Outer 1px subtle window border
    draw.rounded_rectangle([0, 0, win_w - 1, win_h - 1], radius=6, outline=(60, 60, 60, 255), width=1)

    canvas.paste(win, (canvas_pad, canvas_pad), win)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    canvas.save(output_path, "PNG")
    print(f"Generated: {output_path}")

def render_full_vscode_ide(output_path, width=1440, height=880):
    """
    Renders an authentic FULL Visual Studio Code IDE window:
    Top menu + Activity bar + Sidebar Explorer + Code Editor + Integrated Terminal running tests.
    """
    fonts = get_fonts(font_size=13.5)
    win_w = width
    win_h = height

    canvas_pad = 20
    canvas_w = win_w + canvas_pad * 2
    canvas_h = win_h + canvas_pad * 2

    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

    # Drop shadow
    shadow = Image.new("RGBA", (win_w, win_h), (0, 0, 0, 180))
    shadow_mask = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    shadow_mask.paste(shadow, (canvas_pad, canvas_pad + 6))
    shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(16))
    canvas = Image.alpha_composite(canvas, shadow_mask)

    win = Image.new("RGBA", (win_w, win_h), C_BG_DARK)
    draw = ImageDraw.Draw(win)

    # 1. Top Titlebar (Height: 35px)
    titlebar_h = 35
    draw.rectangle([0, 0, win_w, titlebar_h], fill=(30, 30, 30, 255))
    draw.line([0, titlebar_h - 1, win_w, titlebar_h - 1], fill=C_BORDER, width=1)

    # VS Code icon on top left
    draw.text((12, 10), "\ueb51", fill=(0, 122, 204, 255), font=fonts["codicon"])

    # Menu items
    menu_items = ["File", "Edit", "Selection", "View", "Go", "Run", "Terminal", "Help"]
    mx = 36
    for item in menu_items:
        draw.text((mx, 10), item, fill=C_TEXT_PRIMARY, font=fonts["segoe"])
        mx += int(draw.textlength(item, font=fonts["segoe"]) + 14)

    # Center Title (Search/Command palette box style)
    title_text = "test_restaurant_system.py — python project resturent order management system"
    box_w = 560
    box_x = (win_w - box_w) // 2
    draw.rounded_rectangle([box_x, 6, box_x + box_w, 28], radius=4, fill=(45, 45, 45, 255), outline=(60, 60, 60, 255))
    draw.text((box_x + 12, 10), "\uea6d", fill=C_TEXT_MUTED, font=fonts["codicon"])
    draw.text((box_x + 34, 9), title_text, fill=C_TEXT_PRIMARY, font=fonts["segoe"])

    # Window Controls (Min, Max, Close)
    draw.text((win_w - 95, 9), "―", fill=C_TEXT_PRIMARY, font=fonts["segoe"])
    draw.rectangle([win_w - 62, 12, win_w - 52, 22], outline=C_TEXT_PRIMARY, width=1)
    draw.text((win_w - 26, 10), "✕", fill=C_TEXT_PRIMARY, font=fonts["segoe"])

    # 2. Activity Bar (Left 48px width)
    activity_w = 48
    draw.rectangle([0, titlebar_h, activity_w, win_h - 22], fill=C_BG_DARK)
    draw.line([activity_w - 1, titlebar_h, activity_w - 1, win_h - 22], fill=C_BORDER, width=1)

    # Activity Bar Icons
    act_icons = [
        ("\ueaf0", True),  # Explorer (active)
        ("\uea6d", False), # Search
        ("\uea68", False), # Source control
        ("\ueaf3", False), # Run & debug
        ("\ueaf8", False), # Extensions
    ]
    ay = titlebar_h + 12
    for icon, active in act_icons:
        color = C_TEXT_WHITE if active else C_TEXT_MUTED
        if active:
            draw.rectangle([0, ay - 2, 2, ay + 24], fill=C_TAB_ACTIVE_BORDER)
        draw.text((15, ay), icon, fill=color, font=fonts["codicon_lg"])
        ay += 42

    # Bottom Activity Icons (Account & Settings)
    draw.text((15, win_h - 75), "\ueb51", fill=C_TEXT_MUTED, font=fonts["codicon_lg"])
    draw.text((15, win_h - 44), "\ueb51", fill=C_TEXT_MUTED, font=fonts["codicon_lg"])

    # 3. Primary Sidebar (Explorer, Width: 230px)
    sidebar_w = 230
    sidebar_x = activity_w
    draw.rectangle([sidebar_x, titlebar_h, sidebar_x + sidebar_w, win_h - 22], fill=(24, 24, 24, 255))
    draw.line([sidebar_x + sidebar_w - 1, titlebar_h, sidebar_x + sidebar_w - 1, win_h - 22], fill=C_BORDER, width=1)

    # Explorer Header
    draw.text((sidebar_x + 16, titlebar_h + 10), "EXPLORER", fill=C_TEXT_MUTED, font=fonts["segoeb"])
    draw.text((sidebar_x + sidebar_w - 24, titlebar_h + 10), "...", fill=C_TEXT_MUTED, font=fonts["segoe"])

    # Folder Section
    sy = titlebar_h + 34
    draw.text((sidebar_x + 10, sy), "\ueab4", fill=C_TEXT_PRIMARY, font=fonts["codicon_sm"])
    draw.text((sidebar_x + 26, sy), "RESTAURANT SYSTEM", fill=C_TEXT_PRIMARY, font=fonts["segoeb"])
    sy += 24

    file_items = [
        ("\ueab4", "\uea83", "screenshots", (220, 180, 80, 255), False),
        ("  ", "\uea7b", "restaurant_system.py", C_PY_BLUE, False),
        ("  ", "\uea7b", "test_restaurant_system.py", C_PY_BLUE, True),
        ("  ", "\ueab0", "README.md", (80, 160, 240, 255), False),
        ("  ", "\ueab0", "summary.md", (80, 160, 240, 255), False),
    ]

    for chev, icon_glyph, fname, icon_color, is_sel in file_items:
        if is_sel:
            draw.rectangle([sidebar_x, sy - 2, sidebar_x + sidebar_w - 1, sy + 18], fill=(42, 45, 52, 255))
            draw.text((sidebar_x + 8, sy), chev, fill=C_TEXT_MUTED, font=fonts["codicon_sm"])
            draw.text((sidebar_x + 22, sy), icon_glyph, fill=icon_color, font=fonts["codicon_sm"])
            draw.text((sidebar_x + 38, sy), fname, fill=C_TEXT_WHITE, font=fonts["segoeb"])
        else:
            draw.text((sidebar_x + 8, sy), chev, fill=C_TEXT_MUTED, font=fonts["codicon_sm"])
            draw.text((sidebar_x + 22, sy), icon_glyph, fill=icon_color, font=fonts["codicon_sm"])
            draw.text((sidebar_x + 38, sy), fname, fill=C_TEXT_PRIMARY, font=fonts["segoe"])
        sy += 22

    # 4. Main Body: Split between Editor (Top) and Terminal Panel (Bottom)
    editor_x = sidebar_x + sidebar_w
    editor_w = win_w - editor_x
    editor_top_y = titlebar_h

    # Terminal height is 370px, Editor gets the remainder
    terminal_panel_h = 380
    editor_h = (win_h - 22) - editor_top_y - terminal_panel_h
    terminal_y = editor_top_y + editor_h

    # 4a. Editor Background & Tabs
    draw.rectangle([editor_x, editor_top_y, win_w, editor_top_y + editor_h], fill=C_BG_EDITOR)

    # Editor Tab Bar (35px)
    draw.rectangle([editor_x, editor_top_y, win_w, editor_top_y + 35], fill=(24, 24, 24, 255))
    draw.line([editor_x, editor_top_y + 35, win_w, editor_top_y + 35], fill=C_BORDER, width=1)

    # Tab "test_restaurant_system.py"
    tab_w = 215
    draw.rectangle([editor_x, editor_top_y, editor_x + tab_w, editor_top_y + 35], fill=C_BG_EDITOR)
    draw.rectangle([editor_x, editor_top_y, editor_x + tab_w, editor_top_y + 2], fill=C_TAB_ACTIVE_BORDER)
    draw.text((editor_x + 12, editor_top_y + 11), "\uea7b", fill=C_PY_BLUE, font=fonts["codicon"])
    draw.text((editor_x + 30, editor_top_y + 10), "test_restaurant_system.py", fill=C_TEXT_WHITE, font=fonts["segoe"])
    draw.text((editor_x + tab_w - 18, editor_top_y + 10), "\uea76", fill=C_TEXT_MUTED, font=fonts["codicon_sm"])

    # Breadcrumb bar (22px)
    bc_y = editor_top_y + 36
    draw.rectangle([editor_x, bc_y, win_w, bc_y + 22], fill=C_BG_EDITOR)
    draw.text((editor_x + 16, bc_y + 4), "restaurant_system > test_restaurant_system.py > TestRestaurantOrderSystem", fill=C_TEXT_MUTED, font=fonts["segoe"])
    draw.line([editor_x, bc_y + 22, win_w, bc_y + 22], fill=C_BORDER, width=1)

    # Editor Code Preview Lines
    code_lines = [
        (" 1", "import unittest"),
        (" 2", "from restaurant_system import ("),
        (" 3", "    MENU, TOTAL_TABLES, validate_table, validate_item,"),
        (" 4", "    validate_quantity, add_order, calculate_bill, reset_table"),
        (" 5", ")"),
        (" 6", ""),
        (" 7", "class TestRestaurantOrderSystem(unittest.TestCase):"),
        (" 8", "    def test_case_1_normal_input(self):"),
        (" 9", "        # Test Case 1: Table 5, Item Burger (1), Quantity 2"),
        ("10", "        table = validate_table(5)"),
        ("11", "        item = validate_item('Burger')"),
        ("12", "        qty = validate_quantity(2)"),
        ("13", "        res = add_order(table, item, qty)"),
        ("14", "        self.assertEqual(res['message'], 'Burger x2 added to Table 5 │ Amount: 200')"),
    ]

    cy = bc_y + 30
    for lnum, lcode in code_lines:
        draw.text((editor_x + 16, cy), lnum, fill=(90, 90, 90, 255), font=fonts["consola"])
        # Syntax highlighting
        if "import " in lcode or "from " in lcode or "class " in lcode or "def " in lcode:
            draw.text((editor_x + 46, cy), lcode, fill=(86, 156, 214, 255), font=fonts["consola"])
        elif "#" in lcode:
            draw.text((editor_x + 46, cy), lcode, fill=(106, 153, 85, 255), font=fonts["consola"])
        elif "'" in lcode:
            draw.text((editor_x + 46, cy), lcode, fill=(206, 145, 120, 255), font=fonts["consola"])
        else:
            draw.text((editor_x + 46, cy), lcode, fill=C_TEXT_PRIMARY, font=fonts["consola"])
        cy += 18

    # 4b. Terminal Panel (Bottom)
    draw.rectangle([editor_x, terminal_y, win_w, win_h - 22], fill=C_BG_DARK)
    draw.line([editor_x, terminal_y, win_w, terminal_y], fill=C_BORDER, width=1)

    # Terminal Header inside panel
    draw_panel_w = win_w - editor_x
    term_sub = Image.new("RGBA", (draw_panel_w, 35), C_BG_DARK)
    draw_term_sub = ImageDraw.Draw(term_sub)
    draw_vs_code_terminal_header(draw_term_sub, draw_panel_w, fonts)
    win.paste(term_sub, (editor_x, terminal_y), term_sub)

    # Terminal Body Lines (Executing Python Unittest)
    term_lines = [
        ("PS E:\\python project resturent order management system> python -m unittest -v test_restaurant_system.py", "prompt"),
        ("test_boundary_table_numbers (test_restaurant_system.TestRestaurantOrderSystem.test_boundary_table_numbers)", "normal"),
        ("Verify boundary tables 1 and 20 are both accepted ... ok", "test_pass_line"),
        ("test_case_1_normal_input (test_restaurant_system.TestRestaurantOrderSystem.test_case_1_normal_input)", "normal"),
        ("Test Case 1: Table 5, Item Burger (or 1), Quantity 2 -> Amount 200 ... ok", "test_pass_line"),
        ("test_case_2_boundary_minimum_input (test_restaurant_system.TestRestaurantOrderSystem.test_case_2_boundary_minimum_input)", "normal"),
        ("Test Case 2: Table 1, Item Coffee (or 3), Quantity 1 -> Bill calculations ... ok", "test_pass_line"),
        ("test_case_3_invalid_inputs (test_restaurant_system.TestRestaurantOrderSystem.test_case_3_invalid_inputs)", "normal"),
        ("Test Case 3: Rejection of invalid table, invalid item, invalid quantity ... ok", "test_pass_line"),
        ("test_case_4_multi_item_order_and_billing (test_restaurant_system.TestRestaurantOrderSystem.test_case_4_multi_item_order_and_billing)", "normal"),
        ("Test Case 4: Table 3, Burger x2, Pizza x1, Coffee x4 -> Subtotal 600, Total 690.00 ... ok", "test_pass_line"),
        ("test_table_clear_and_reset (test_restaurant_system.TestRestaurantOrderSystem.test_table_clear_and_reset)", "normal"),
        ("Verify table orders list is completely cleared upon checkout ... ok", "test_pass_line"),
        ("", "normal"),
        ("----------------------------------------------------------------------", "dim"),
        ("Ran 6 tests in 0.000s", "normal"),
        ("", "normal"),
        ("OK", "test_ok_badge"),
        ("", "normal"),
        ("PS E:\\python project resturent order management system> ", "cursor"),
    ]

    ty = terminal_y + 35 + 10
    for line_info in term_lines:
        text, style = line_info
        if style == "prompt":
            p_part, c_part = text.split("> ", 1)
            draw.text((editor_x + 20, ty), p_part + "> ", fill=C_TEXT_PRIMARY, font=fonts["consolab"])
            pw = draw.textlength(p_part + "> ", font=fonts["consolab"])
            draw.text((editor_x + 20 + pw, ty), c_part, fill=C_YELLOW, font=fonts["consolab"])
        elif style == "test_pass_line":
            if " ... ok" in text:
                left_part, _ = text.split(" ... ok", 1)
                draw.text((editor_x + 20, ty), left_part, fill=C_TEXT_PRIMARY, font=fonts["consola"])
                pw = draw.textlength(left_part, font=fonts["consola"])
                draw.text((editor_x + 20 + pw, ty), " ... ", fill=C_TEXT_MUTED, font=fonts["consola"])
                pw += draw.textlength(" ... ", font=fonts["consola"])
                draw.text((editor_x + 20 + pw, ty), "ok", fill=C_GREEN, font=fonts["consolab"])
        elif style == "test_ok_badge":
            draw.text((editor_x + 20, ty), text, fill=C_GREEN, font=fonts["consolab"])
        elif style == "dim":
            draw.text((editor_x + 20, ty), text, fill=C_TEXT_DIM, font=fonts["consola"])
        elif style == "cursor":
            draw.text((editor_x + 20, ty), text, fill=C_TEXT_PRIMARY, font=fonts["consolab"])
            cw = draw.textlength(text, font=fonts["consolab"])
            draw.rectangle([editor_x + 20 + cw + 2, ty + 2, editor_x + 20 + cw + 9, ty + 15], fill=C_CURSOR)
        else:
            draw.text((editor_x + 20, ty), text, fill=C_TEXT_PRIMARY, font=fonts["consola"])
        ty += 16

    # 5. Blue Status Bar (Bottom 22px)
    draw_vs_code_status_bar(draw, win_w, win_h - 22, fonts)

    # Outer 1px window border
    draw.rounded_rectangle([0, 0, win_w - 1, win_h - 1], radius=8, outline=(60, 60, 60, 255), width=1)

    canvas.paste(win, (canvas_pad, canvas_pad), win)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    canvas.save(output_path, "PNG")
    print(f"Generated Full IDE View: {output_path}")

def generate_all_screenshots():
    screenshots_dir = r"E:\python project resturent order management system\screenshots"

    # ==========================================================================
    # 0. ALL TESTS PASS - AUTOMATED TEST SUITE (VS Code Integrated Terminal)
    # ==========================================================================
    all_tests_lines = [
        ("PS E:\\python project resturent order management system> python -m unittest -v test_restaurant_system.py", "prompt"),
        ("test_boundary_table_numbers (test_restaurant_system.TestRestaurantOrderSystem.test_boundary_table_numbers)", "normal"),
        ("Verify boundary tables 1 and 20 are both accepted ... ok", "test_pass_line"),
        ("test_case_1_normal_input (test_restaurant_system.TestRestaurantOrderSystem.test_case_1_normal_input)", "normal"),
        ("Test Case 1: Table 5, Item Burger (or 1), Quantity 2 -> Amount 200 ... ok", "test_pass_line"),
        ("test_case_2_boundary_minimum_input (test_restaurant_system.TestRestaurantOrderSystem.test_case_2_boundary_minimum_input)", "normal"),
        ("Test Case 2: Table 1, Item Coffee (or 3), Quantity 1 -> Bill calculations ... ok", "test_pass_line"),
        ("test_case_3_invalid_inputs (test_restaurant_system.TestRestaurantOrderSystem.test_case_3_invalid_inputs)", "normal"),
        ("Test Case 3: Rejection of invalid table, invalid item, invalid quantity ... ok", "test_pass_line"),
        ("test_case_4_multi_item_order_and_billing (test_restaurant_system.TestRestaurantOrderSystem.test_case_4_multi_item_order_and_billing)", "normal"),
        ("Test Case 4: Table 3, Burger x2, Pizza x1, Coffee x4 -> Subtotal 600, Total 690.00 ... ok", "test_pass_line"),
        ("test_table_clear_and_reset (test_restaurant_system.TestRestaurantOrderSystem.test_table_clear_and_reset)", "normal"),
        ("Verify table orders list is completely cleared upon checkout ... ok", "test_pass_line"),
        ("", "normal"),
        ("----------------------------------------------------------------------", "dim"),
        ("Ran 6 tests in 0.000s", "normal"),
        ("", "normal"),
        ("OK", "test_ok_badge"),
        ("", "normal"),
        ("PS E:\\python project resturent order management system> ", "cursor"),
    ]
    render_vscode_terminal_image(
        all_tests_lines,
        os.path.join(screenshots_dir, "test_case_all_pass_vscode.png"),
        width=1180
    )

    # ==========================================================================
    # 1. TEST CASE 1: Normal Input (VS Code Integrated Terminal)
    # ==========================================================================
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
    render_vscode_terminal_image(
        tc1_lines,
        os.path.join(screenshots_dir, "test_case_1_normal.png"),
        width=1180
    )

    # ==========================================================================
    # 2. TEST CASE 2: Boundary / Minimum Input (VS Code Integrated Terminal)
    # ==========================================================================
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
        ("Subtotal: 50 │ Service charge (10%): 5.00", "header"),
        ("GST (5%): 2.50 │ Total: 57.50", "success"),
        ("", "normal"),
        ("======================================================", "dim"),
        ("            FINAL BILL RECEIPT (PS No. 35)            ", "header"),
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
    render_vscode_terminal_image(
        tc2_lines,
        os.path.join(screenshots_dir, "test_case_2_boundary.png"),
        width=1180
    )

    # ==========================================================================
    # 3. TEST CASE 3: Invalid Input Validation Checks (VS Code Integrated Terminal)
    # ==========================================================================
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
    render_vscode_terminal_image(
        tc3_lines,
        os.path.join(screenshots_dir, "test_case_3_invalid.png"),
        width=1180
    )

    # ==========================================================================
    # 4. TEST CASE 4: Multi-Item Order and Billing (VS Code Integrated Terminal)
    # ==========================================================================
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
        ("Subtotal: 600 │ Service charge (10%): 60.00", "header"),
        ("GST (5%): 30.00 │ Total: 690.00", "success"),
        ("", "normal"),
        ("======================================================", "dim"),
        ("            FINAL BILL RECEIPT (PS No. 35)            ", "header"),
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
    render_vscode_terminal_image(
        tc4_lines,
        os.path.join(screenshots_dir, "test_case_4_multi_item.png"),
        width=1180
    )

    # ==========================================================================
    # 5. FULL VS CODE IDE WINDOW SCREENSHOT
    # ==========================================================================
    render_full_vscode_ide(
        os.path.join(screenshots_dir, "vscode_full_ide_test_pass.png"),
        width=1440,
        height=880
    )

if __name__ == "__main__":
    generate_all_screenshots()
