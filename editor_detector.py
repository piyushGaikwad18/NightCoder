import os
import pyautogui
import pytesseract

from pytesseract import Output
from difflib import SequenceMatcher


# ============================================================
# SETTINGS
# ============================================================

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

EXPLORER_END_X = 350

TAB_MIN_Y = 30
TAB_MAX_Y = 110

# Distance below detected tab where the editor is expected
EDITOR_OFFSET_Y = 100

SUPPORTED_EXTENSIONS = (
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".java",
    ".json",
    ".html",
    ".css",
    ".md",
    ".txt",
)


# ============================================================
# NORMALIZATION
# ============================================================

def normalize(text):
    text = text.lower().strip()

    # OCR sometimes removes spaces around filenames
    text = text.replace(" ", "")

    return text


def similarity(a, b):
    return SequenceMatcher(
        None,
        normalize(a),
        normalize(b)
    ).ratio()


# ============================================================
# OCR
# ============================================================

def read_tabs():

    screenshot = pyautogui.screenshot()

    data = pytesseract.image_to_data(
        screenshot,
        output_type=Output.DICT,
        config="--psm 11"
    )

    results = []

    for i, text in enumerate(data["text"]):

        text = text.strip()

        if not text:
            continue

        try:
            confidence = float(
                data["conf"][i]
            )
        except (ValueError, TypeError):
            continue

        if confidence < 40:
            continue

        x = data["left"][i]
        y = data["top"][i]

        width = data["width"][i]
        height = data["height"][i]

        results.append({
            "text": text,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "center_x": x + width // 2,
            "center_y": y + height // 2,
            "confidence": confidence,
        })

    return results


# ============================================================
# FILE DETECTION
# ============================================================

def looks_like_file(text):

    text = normalize(text)

    return text.endswith(
        SUPPORTED_EXTENSIONS
    )


# ============================================================
# FIND TARGET TAB
# ============================================================

def find_active_tab(target):

    screen_width, screen_height = (
        pyautogui.size()
    )

    target_normalized = normalize(target)

    results = read_tabs()

    candidates = []

    for item in results:

        text = item["text"]

        x = item["center_x"]
        y = item["center_y"]

        # Must be in editor area
        if x <= EXPLORER_END_X:
            continue

        # Must be in tab strip
        if y < TAB_MIN_Y:
            continue

        if y > TAB_MAX_Y:
            continue

        # Ignore extreme right controls
        if x > screen_width * 0.95:
            continue

        # Must look like a filename
        if not looks_like_file(text):
            continue

        score = similarity(
            target_normalized,
            text
        )

        # Exact match
        if normalize(text) == target_normalized:

            print(
                f"Exact tab match: {text}"
            )

            return {
                **item,
                "similarity": 1.0,
                "score": 100
            }

        # Fuzzy match
        if score >= 0.65:

            candidates.append({
                **item,
                "similarity": score,
                "score": score * 100
            })

    if not candidates:
        return None

    candidates.sort(
        key=lambda item: (
            item["similarity"],
            item["confidence"]
        ),
        reverse=True
    )

    best = candidates[0]

    print(
        f'Fuzzy tab match: '
        f'{best["text"]}'
    )

    return best


# ============================================================
# FIND EDITOR FROM TARGET TAB
# ============================================================

def find_editor(target):

    screen_width, screen_height = (
        pyautogui.size()
    )

    tab = find_active_tab(target)

    if not tab:
        return None

    # Editor point is dynamically derived
    # from the detected tab position.

    editor_x = tab["center_x"]

    editor_y = (
        tab["y"]
        +
        tab["height"]
        +
        EDITOR_OFFSET_Y
    )

    # Keep inside usable editor area

    editor_x = max(
        EXPLORER_END_X + 50,
        editor_x
    )

    editor_x = min(
        editor_x,
        int(screen_width * 0.90)
    )

    editor_y = max(
        130,
        editor_y
    )

    editor_y = min(
        editor_y,
        int(screen_height * 0.70)
    )

    return {
        "x": int(editor_x),
        "y": int(editor_y),

        "tab_text": tab["text"],

        "tab_x": tab["center_x"],
        "tab_y": tab["center_y"],

        "confidence": tab["confidence"],

        "similarity": tab["similarity"],

        "score": tab["score"],
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("NightCoder Editor Detector")
    print("--------------------------")
    print()

    target = input(
        "Enter target filename: "
    ).strip()

    if not target:

        print(
            "❌ No target provided."
        )

        raise SystemExit

    print()

    print(
        f'Looking for tab: "{target}"'
    )

    print()

    result = find_editor(target)

    print()

    if not result:

        print(
            "❌ Target tab was not found."
        )

        print(
            "NightCoder will NOT move the mouse."
        )

    else:

        print(
            "TARGET TAB FOUND"
        )

        print(
            "----------------"
        )

        print(
            f'Tab: '
            f'{result["tab_text"]}'
        )

        print(
            f'Tab position: '
            f'({result["tab_x"]}, '
            f'{result["tab_y"]})'
        )

        print(
            f'Editor candidate: '
            f'({result["x"]}, '
            f'{result["y"]})'
        )

        print(
            f'Tab confidence: '
            f'{result["confidence"]:.0f}%'
        )

        print(
            f'Similarity: '
            f'{result["similarity"]:.2f}'
        )

        print()

        answer = input(
            "Move mouse to editor candidate? (y/n): "
        ).strip().lower()

        if answer == "y":

            print(
                "Moving mouse..."
            )

            pyautogui.moveTo(
                result["x"],
                result["y"],
                duration=0.25
            )

            print(
                "Mouse moved."
            )

        else:

            print(
                "Mouse movement cancelled."
            )