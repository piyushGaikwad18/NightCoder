import os

import pyautogui
import pytesseract

from pytesseract import Output
from PIL import (
    ImageEnhance,
    ImageFilter,
    ImageOps,
)


# ============================================================
# SETTINGS
# ============================================================

TESSERACT_PATH = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

EXPLORER_REGION = (
    0,      # left
    80,     # top
    350,    # right
    700     # bottom
)

SCALE = 3


# ============================================================
# TESSERACT
# ============================================================

if not os.path.exists(TESSERACT_PATH):

    raise FileNotFoundError(
        "Tesseract was not found at:\n"
        f"{TESSERACT_PATH}"
    )


pytesseract.pytesseract.tesseract_cmd = (
    TESSERACT_PATH
)


# ============================================================
# CAPTURE
# ============================================================

def capture_explorer():

    screenshot = pyautogui.screenshot()

    explorer = screenshot.crop(
        EXPLORER_REGION
    )

    return explorer


# ============================================================
# CREATE OCR VARIANTS
# ============================================================

def create_variants(image):

    width, height = image.size

    # --------------------------------------------------------
    # Variant 1
    # Enlarged grayscale + sharpen
    # --------------------------------------------------------

    normal = image.resize(
        (
            width * SCALE,
            height * SCALE
        )
    )

    normal = normal.convert("L")

    normal = normal.filter(
        ImageFilter.SHARPEN
    )

    normal = ImageEnhance.Contrast(
        normal
    ).enhance(2.0)


    # --------------------------------------------------------
    # Variant 2
    # Strong contrast
    # --------------------------------------------------------

    high_contrast = image.resize(
        (
            width * SCALE,
            height * SCALE
        )
    )

    high_contrast = high_contrast.convert(
        "L"
    )

    high_contrast = ImageEnhance.Contrast(
        high_contrast
    ).enhance(3.0)

    high_contrast = high_contrast.filter(
        ImageFilter.SHARPEN
    )


    # --------------------------------------------------------
    # Variant 3
    # Threshold
    # --------------------------------------------------------

    threshold = ImageOps.grayscale(
        image.resize(
            (
                width * SCALE,
                height * SCALE
            )
        )
    )

    threshold = ImageOps.autocontrast(
        threshold
    )

    threshold = threshold.point(
        lambda pixel:
        255 if pixel > 145 else 0
    )


    return [
        (
            "normal",
            normal,
            "--psm 6"
        ),
        (
            "high_contrast",
            high_contrast,
            "--psm 6"
        ),
        (
            "threshold",
            threshold,
            "--psm 11"
        ),
    ]


# ============================================================
# RUN ONE OCR PASS
# ============================================================

def run_ocr(image, config):

    data = pytesseract.image_to_data(
        image,
        output_type=Output.DICT,
        config=config
    )

    results = []

    for i, text in enumerate(
        data["text"]
    ):

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

        if confidence < 20:

            continue

        x = data["left"][i]
        y = data["top"][i]

        width = data["width"][i]
        height = data["height"][i]

        # Convert enlarged-image coordinates
        # back into screen coordinates.

        screen_x = (
            EXPLORER_REGION[0]
            +
            (x + width // 2) // SCALE
        )

        screen_y = (
            EXPLORER_REGION[1]
            +
            (y + height // 2) // SCALE
        )

        results.append(
            {
                "text": text,
                "x": screen_x,
                "y": screen_y,
                "confidence": confidence,
            }
        )

    return results


# ============================================================
# MULTI-PASS OCR
# ============================================================

def read_explorer():

    original = capture_explorer()

    variants = create_variants(
        original
    )

    all_results = []

    for name, image, config in variants:

        results = run_ocr(
            image,
            config
        )

        for result in results:

            result["pass"] = name

            all_results.append(
                result
            )

    return all_results


# ============================================================
# PRINT RESULTS
# ============================================================

def print_results(results):

    print()
    print("=" * 70)
    print("MULTI-PASS EXPLORER OCR RESULTS")
    print("=" * 70)
    print()

    if not results:

        print(
            "No text detected."
        )

        return

    for index, item in enumerate(
        results,
        start=1
    ):

        print(
            f"{index:>3}. "
            f'{item["text"]:<25} '
            f'position=({item["x"]}, '
            f'{item["y"]}) '
            f'confidence='
            f'{item["confidence"]:.0f}% '
            f'pass={item["pass"]}'
        )

    print()
    print(
        f"Total OCR results: "
        f"{len(results)}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print()
    print("NightCoder Explorer Reader")
    print("--------------------------")
    print()

    print(
        "Running multi-pass Explorer OCR..."
    )

    results = read_explorer()

    print_results(
        results
    )

    print()
    print(
        "Multi-pass OCR test complete."
    )