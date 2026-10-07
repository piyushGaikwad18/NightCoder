import os
import pyautogui
import pytesseract
from pytesseract import Output


# --------------------------------------------------
# Tesseract configuration
# --------------------------------------------------

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if not os.path.exists(TESSERACT_PATH):
    raise FileNotFoundError(
        f"Tesseract was not found at:\n{TESSERACT_PATH}"
    )

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# --------------------------------------------------
# Read screen
# --------------------------------------------------

def read_screen():

    screenshot = pyautogui.screenshot()

    data = pytesseract.image_to_data(
        screenshot,
        output_type=Output.DICT
    )

    results = []

    for i, text in enumerate(data["text"]):

        text = text.strip()

        if not text:
            continue

        try:
            confidence = float(data["conf"][i])
        except (ValueError, TypeError):
            continue

        if confidence < 40:
            continue

        x = data["left"][i]
        y = data["top"][i]
        width = data["width"][i]
        height = data["height"][i]

        center_x = x + width // 2
        center_y = y + height // 2

        results.append({
            "text": text,
            "x": center_x,
            "y": center_y,
            "confidence": confidence
        })

    return results


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    print("NightCoder Screen Reader")
    print("------------------------")
    print("Tesseract:", TESSERACT_PATH)
    print("Reading screen...")
    print()

    results = read_screen()

    if not results:

        print("No readable text detected.")

    else:

        print("Detected text:")
        print()

        for item in results:

            print(
                f'{item["text"]:<25} '
                f'position=({item["x"]}, {item["y"]}) '
                f'confidence={item["confidence"]:.0f}%'
            )

    print()
    print(f"Total detected words: {len(results)}")