import time
import pyautogui

from target_finder import find_target
from mouse_controller import smooth_move_to
from keyboard_controller import type_text, save
from verification import is_text_visible
from editor_detector import find_editor
from terminal_controller import open_terminal, run_command


# ============================================================
# OPEN FILE
# ============================================================

def open_file(target):

    print()
    print("=" * 50)
    print(f"Opening: {target}")
    print("=" * 50)

    result = find_target(target)

    if not result:

        print()
        print("❌ No safe Explorer match found.")
        print("NightCoder will NOT click anything.")

        return False

    x = result["x"]
    y = result["y"]

    print(
        f'Found: {result["text"]}'
    )

    print(
        f'Position: ({x}, {y})'
    )

    print(
        f'Similarity: '
        f'{result["similarity"]:.2f}'
    )

    print(
        "Moving mouse to file..."
    )

    smooth_move_to(x, y)

    time.sleep(0.2)

    print(
        "Double-clicking..."
    )

    pyautogui.doubleClick(
        interval=0.1
    )

    time.sleep(1)

    print(
        "Verifying file..."
    )

    if not is_text_visible(
        target,
        wait=2,
        threshold=0.70
    ):

        print(
            "❌ File verification failed."
        )

        return False

    print(
        "✅ File verified."
    )

    return True


# ============================================================
# FOCUS EDITOR
# ============================================================

def focus_editor(target):

    print()
    print("=" * 50)
    print("Finding editor")
    print("=" * 50)

    print(
        f'Looking for active tab: "{target}"'
    )

    time.sleep(0.5)

    result = find_editor(target)

    if not result:

        print()
        print(
            "❌ Could not find target editor tab."
        )

        print(
            "NightCoder will NOT click."
        )

        return False

    print()

    print(
        f'Tab found: {result["tab_text"]}'
    )

    print(
        f'Similarity: '
        f'{result["similarity"]:.2f}'
    )

    print(
        f'Confidence: '
        f'{result["confidence"]:.0f}%'
    )

    print(
        f'Editor position: '
        f'({result["x"]}, {result["y"]})'
    )

    print(
        "Moving mouse to editor..."
    )

    smooth_move_to(
        result["x"],
        result["y"]
    )

    time.sleep(0.2)

    print(
        "Clicking editor..."
    )

    pyautogui.click()

    time.sleep(0.3)

    print(
        "✅ Editor focused."
    )

    return True


# ============================================================
# TYPE TEST CODE
# ============================================================

def type_test():

    print()
    print("=" * 50)
    print("Typing code")
    print("=" * 50)

    test_code = (
        'print("NightCoder typing test")'
    )

    print(
        f"Code: {test_code}"
    )

    # Start at the beginning of the current line
    pyautogui.press("home")

    time.sleep(0.2)

    print(
        "Typing..."
    )

    type_text(test_code)

    time.sleep(0.5)

    print(
        "Saving..."
    )

    save()

    time.sleep(1)

    print(
        "✅ Code saved."
    )


# ============================================================
# RUN FILE
# ============================================================

def run_file(target):

    print()
    print("=" * 50)
    print("Running program")
    print("=" * 50)

    # --------------------------------------------------------
    # Open integrated terminal
    # --------------------------------------------------------

    open_terminal()

    time.sleep(0.5)

    # --------------------------------------------------------
    # Run Python file
    # --------------------------------------------------------

    command = f"python {target}"

    run_command(
        command,
        wait_time=2
    )

    print()
    print(
        "✅ Program execution finished."
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("========================================")
    print("          NIGHTCODER")
    print("       FULL GUI TEST")
    print("========================================")
    print()

    target = input(
        "Enter Python file to open: "
    ).strip()

    if not target:

        print(
            "❌ No file entered."
        )

        return

    # ========================================================
    # STEP 1 — OPEN FILE
    # ========================================================

    success = open_file(target)

    if not success:

        print(
            "❌ NightCoder stopped."
        )

        return

    # ========================================================
    # STEP 2 — FIND EDITOR
    # ========================================================

    success = focus_editor(target)

    if not success:

        print(
            "❌ NightCoder stopped."
        )

        return

    # ========================================================
    # STEP 3 — TYPE
    # ========================================================

    print()
    print(
        "Starting typing in 1 second..."
    )

    time.sleep(1)

    type_test()

    # ========================================================
    # STEP 4 — RUN
    # ========================================================

    print()
    print(
        "Starting program in 1 second..."
    )

    time.sleep(1)

    run_file(target)

    # ========================================================
    # FINISHED
    # ========================================================

    print()
    print("========================================")
    print("      NIGHTCODER TEST COMPLETE")
    print("========================================")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()