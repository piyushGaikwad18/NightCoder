import pyautogui
from pathlib import Path
from datetime import datetime


SCREENSHOT_DIR = Path("screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)


def capture_screen():
    """
    Capture the current Windows screen and save it.
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = SCREENSHOT_DIR / f"screen_{timestamp}.png"

    screenshot = pyautogui.screenshot()

    screenshot.save(filename)

    print(f"Screenshot saved:")
    print(filename)

    return filename


if __name__ == "__main__":
    print("NightCoder Screen Observer")
    print("--------------------------")
    print("Capturing screen...")

    file_path = capture_screen()

    print()
    print("Done.")