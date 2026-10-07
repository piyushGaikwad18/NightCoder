import time
import random
import pyautogui


def type_text(text):
    """
    Type text visibly into the currently focused application.
    """

    for char in text:

        pyautogui.write(
            char,
            interval=0
        )

        # Small natural variation
        time.sleep(random.uniform(0.005, 0.018))


def press_key(key):
    """
    Press a single keyboard key.
    """

    pyautogui.press(key)


def hotkey(*keys):
    """
    Press a keyboard shortcut.

    Example:
        hotkey("ctrl", "s")
    """

    pyautogui.hotkey(*keys)


def select_all():
    """
    Select everything in the current editor.
    """

    hotkey("ctrl", "a")


def save():
    """
    Save the current file.
    """

    hotkey("ctrl", "s")


def clear_editor():
    """
    Select all text and delete it.
    """

    select_all()
    time.sleep(0.1)
    press_key("backspace")


if __name__ == "__main__":

    print("NightCoder Keyboard Controller")
    print("--------------------------------")

    print("Click your text editor within 5 seconds...")

    time.sleep(5)

    print("Typing test...")

    type_text(
        "print('Hello from NightCoder!')"
    )

    print("Done.")