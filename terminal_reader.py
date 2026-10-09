import os
import time
import pyautogui
import pytesseract

from pytesseract import Output


# ============================================================
# TESSERACT
# ============================================================

TESSERACT_PATH = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

if not os.path.exists(TESSERACT_PATH):
    raise FileNotFoundError(
        f"Tesseract not found:\n{TESSERACT_PATH}"
    )

pytesseract.pytesseract.tesseract_cmd = (
    TESSERACT_PATH
)


# ============================================================
# TERMINAL HEADER
# ============================================================

def find_terminal_header():

    screenshot = pyautogui.screenshot()

    data = pytesseract.image_to_data(
        screenshot,
        output_type=Output.DICT,
        config="--psm 11"
    )

    candidates = []

    for i, text in enumerate(data["text"]):

        text = text.strip()

        if not text:
            continue

        try:
            confidence = float(
                data["conf"][i]
            )
        except (
            ValueError,
            TypeError
        ):
            continue

        if confidence < 45:
            continue

        if text.lower() != "terminal":
            continue

        x = data["left"][i]
        y = data["top"][i]

        width = data["width"][i]
        height = data["height"][i]

        candidates.append({
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "confidence": confidence
        })

    if not candidates:
        return None

    # Prefer the lowest Terminal label.
    candidates.sort(
        key=lambda item: item["y"],
        reverse=True
    )

    return candidates[0]


# ============================================================
# CAPTURE TERMINAL
# ============================================================

def capture_terminal():

    screenshot = pyautogui.screenshot()

    screen_width, screen_height = (
        screenshot.size
    )

    header = find_terminal_header()

    if header:

        # Start below the Terminal header.
        top = (
            header["y"]
            +
            header["height"]
            +
            5
        )

        # Terminal extends to the bottom.
        left = max(
            0,
            int(screen_width * 0.25)
        )

        right = screen_width

        bottom = screen_height

        return screenshot.crop(
            (
                left,
                top,
                right,
                bottom
            )
        )

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    print(
        "⚠️ Terminal header not detected."
    )

    return screenshot.crop(
        (
            int(screen_width * 0.25),
            int(screen_height * 0.68),
            screen_width,
            screen_height
        )
    )


# ============================================================
# READ TERMINAL
# ============================================================

def read_terminal():

    terminal = capture_terminal()

    text = pytesseract.image_to_string(
        terminal,
        config="--psm 6"
    )

    return text.strip()


# ============================================================
# ERROR DETECTION
# ============================================================

def contains_error(text):

    error_markers = [
        "Traceback",
        "SyntaxError",
        "NameError",
        "TypeError",
        "ValueError",
        "IndexError",
        "KeyError",
        "AttributeError",
        "ImportError",
        "ModuleNotFoundError",
        "FileNotFoundError",
        "IndentationError",
        "Exception",
    ]

    text_lower = text.lower()

    for marker in error_markers:

        if marker.lower() in text_lower:
            return True

    return False


# ============================================================
# SUCCESS DETECTION
# ============================================================

def contains_success(text):

    success_markers = [
        "NightCoder typing test",
        "process exited",
        "success",
        "completed",
    ]

    text_lower = text.lower()

    for marker in success_markers:

        if marker.lower() in text_lower:
            return True

    return False


# ============================================================
# ANALYZE RESULT
# ============================================================

def analyze_terminal():

    text = read_terminal()

    print()
    print("TERMINAL OUTPUT")
    print("-" * 50)

    print(text)

    print("-" * 50)

    if contains_error(text):

        return {
            "status": "error",
            "text": text
        }

    if contains_success(text):

        return {
            "status": "success",
            "text": text
        }

    return {
        "status": "unknown",
        "text": text
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 50)
    print("NightCoder Terminal Reader")
    print("=" * 50)

    print()
    print("Reading terminal...")

    time.sleep(1)

    result = analyze_terminal()

    print()

    if result["status"] == "success":

        print(
            "✅ SUCCESS DETECTED"
        )

    elif result["status"] == "error":

        print(
            "❌ ERROR DETECTED"
        )

    else:

        print(
            "⚠️ Result unclear"
        )