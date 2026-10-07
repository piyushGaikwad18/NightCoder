import time
import pyautogui

from target_finder import find_target
from mouse_controller import smooth_move_to
from keyboard_controller import type_text, save
from verification import is_text_visible


def open_file(target):
    """
    Find a file on screen, move to it, click it,
    and verify that it is visible.
    """

    print()
    print("=" * 50)
    print(f"Opening: {target}")
    print("=" * 50)

    # --------------------------------------------------
    # Find target
    # --------------------------------------------------

    result = find_target(target)

    if not result:
        print("❌ Target not found.")
        return False

    x = result["x"]
    y = result["y"]

    print(f"Found: {result['text']}")
    print(f"Position: ({x}, {y})")
    print(
        f"Similarity: "
        f"{result['similarity']:.2f}"
    )

    # --------------------------------------------------
    # Move mouse
    # --------------------------------------------------

    print("Moving mouse...")

    smooth_move_to(x, y)

    time.sleep(0.2)

    # --------------------------------------------------
    # Click
    # --------------------------------------------------

    print("Clicking...")

    pyautogui.click()

    time.sleep(0.8)

    # --------------------------------------------------
    # Verify
    # --------------------------------------------------

    print("Verifying...")

    if is_text_visible(
        target,
        wait=2,
        threshold=0.70
    ):

        print("✅ File verified.")

        return True

    print("❌ File verification failed.")

    return False


def type_test():

    print()
    print("=" * 50)
    print("Typing test")
    print("=" * 50)

    # Click inside editor first
    pyautogui.click()

    time.sleep(0.2)

    test_code = (
        "\n"
        "# NightCoder test\n"
        "print('NightCoder is working!')\n"
    )

    print("Typing test code...")

    type_text(test_code)

    time.sleep(0.3)

    print("Saving...")

    save()

    time.sleep(0.5)

    print("✅ Typing test complete.")


def main():

    print()
    print("========================================")
    print("          NIGHTCODER")
    print("      GUI Automation Test")
    print("========================================")
    print()

    target = input(
        "Enter file to open: "
    ).strip()

    if not target:
        print("No target entered.")
        return

    # --------------------------------------------------
    # Open and verify file
    # --------------------------------------------------

    success = open_file(target)

    if not success:

        print()
        print("❌ NightCoder stopped.")
        print("File could not be verified.")

        return

    # --------------------------------------------------
    # Ask before typing
    # --------------------------------------------------

    print()
    print("File successfully opened.")
    print()

    answer = input(
        "Run typing test? (y/n): "
    ).strip().lower()

    if answer == "y":

        type_test()

    else:

        print("Typing test skipped.")

    print()
    print("========================================")
    print("NightCoder test finished.")
    print("========================================")


if __name__ == "__main__":
    main()