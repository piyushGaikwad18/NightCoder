import time
import pyautogui
import pytesseract
from pytesseract import Output
from difflib import SequenceMatcher


# --------------------------------------------------
# Tesseract configuration
# --------------------------------------------------

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# --------------------------------------------------
# Similarity
# --------------------------------------------------

def similarity(a, b):
    return SequenceMatcher(
        None,
        a.lower(),
        b.lower()
    ).ratio()


# --------------------------------------------------
# Read screen
# --------------------------------------------------

def get_screen_words():

    screenshot = pyautogui.screenshot()

    data = pytesseract.image_to_data(
        screenshot,
        output_type=Output.DICT
    )

    words = []

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

        words.append(text)

    return words


# --------------------------------------------------
# Verify target
# --------------------------------------------------

def is_text_visible(
    target,
    wait=3,
    threshold=0.70
):

    print(f"Verifying: {target}")

    start_time = time.time()

    target_lower = target.lower()

    while time.time() - start_time < wait:

        words = get_screen_words()

        # First: exact match
        for word in words:

            if word.lower() == target_lower:

                print(
                    f"✓ Exact match: {word}"
                )

                return True

        # Second: fuzzy match
        for word in words:

            score = similarity(
                target,
                word
            )

            if score >= threshold:

                print(
                    f"✓ Fuzzy match: "
                    f"{word} "
                    f"(similarity={score:.2f})"
                )

                return True

        time.sleep(0.3)

    print(
        f"✗ Could not verify: {target}"
    )

    return False


# --------------------------------------------------
# Wait for target
# --------------------------------------------------

def wait_for_text(
    target,
    timeout=5,
    threshold=0.70
):

    print(f"Waiting for: {target}")

    start_time = time.time()

    while time.time() - start_time < timeout:

        if is_text_visible(
            target,
            wait=0.5,
            threshold=threshold
        ):

            return True

        time.sleep(0.2)

    return False


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    print("NightCoder Verification")
    print("-----------------------")

    target = input(
        "Enter text currently visible on screen: "
    )

    print()

    result = is_text_visible(target)

    print()

    if result:

        print("Verification successful.")

    else:

        print("Verification failed.")