import time

from target_finder import find_target
from mouse_controller import smooth_move_to
import pyautogui


def click_target(target):
    print(f"Searching for: {target}")

    result = find_target(target)

    if not result:
        print("Target not found.")
        return False

    x = result["x"]
    y = result["y"]

    print(f"Found: {result['text']}")
    print(f"Position: ({x}, {y})")
    print(f"Similarity: {result['similarity']:.2f}")

    print("Moving mouse...")

    smooth_move_to(x, y)

    time.sleep(0.15)

    print("Clicking...")

    pyautogui.click()

    print("Clicked successfully.")

    return True


if __name__ == "__main__":

    print("NightCoder Click Target")
    print("-----------------------")

    target = input("Enter target to click: ")

    print()

    click_target(target)