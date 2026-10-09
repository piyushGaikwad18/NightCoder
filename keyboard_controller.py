import time
import random
import pyautogui


def type_text(text):
    """
    Type text with tiny natural delays.
    """

    for char in text:

        # pyautogui.write handles normal
        # keyboard characters.

        pyautogui.write(
            char,
            interval=0
        )

        time.sleep(
            random.uniform(
                0.005,
                0.018
            )
        )


def press_key(key):
    pyautogui.press(key)


def hotkey(*keys):
    pyautogui.hotkey(*keys)


def select_all():
    hotkey("ctrl", "a")


def save():
    hotkey("ctrl", "s")


def clear_editor():
    select_all()

    time.sleep(0.1)

    press_key("backspace")