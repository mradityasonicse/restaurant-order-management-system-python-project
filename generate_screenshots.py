"""
Screenshot generator entry point.
Invokes build_vscode_screenshots.py to produce authentic VS Code terminal screenshots.
"""

from build_vscode_screenshots import generate_all_screenshots

if __name__ == "__main__":
    generate_all_screenshots()
