import time
import pyautogui

from keyboard_controller import type_text


# ============================================================
# OPEN TERMINAL
# ============================================================

def open_terminal():
    print()
    print("Opening VS Code terminal...")

    # VS Code integrated terminal shortcut
    pyautogui.hotkey("ctrl", "`")

    time.sleep(1)

    print("✅ Terminal opened.")


# ============================================================
# RUN COMMAND
# ============================================================

def run_command(command, wait_time=2):

    print()
    print(f"Running command:")
    print(f"> {command}")
    print()

    type_text(command)

    pyautogui.press("enter")

    print("Command executed.")

    time.sleep(wait_time)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 50)
    print("NightCoder Terminal Controller")
    print("=" * 50)

    print()
    print("Make sure VS Code is open.")
    print("The integrated terminal will be opened automatically.")

    time.sleep(2)

    open_terminal()

    run_command(
        "python --version"
    )

    print()
    print("=" * 50)
    print("Terminal test finished.")
    print("=" * 50)