from screen_reader import read_screen
from difflib import SequenceMatcher


def similarity(a, b):
    return SequenceMatcher(
        None,
        a.lower(),
        b.lower()
    ).ratio()


def find_target(target, threshold=0.60):
    """
    Find a target text on the screen using OCR.

    Example:
        find_target("automation.py")
    """

    results = read_screen()

    best_match = None
    best_score = 0

    for item in results:
        text = item["text"]

        score = similarity(target, text)

        if score > best_score:
            best_score = score
            best_match = item

    if best_match and best_score >= threshold:
        return {
            "text": best_match["text"],
            "x": best_match["x"],
            "y": best_match["y"],
            "confidence": best_match["confidence"],
            "similarity": best_score
        }

    return None


if __name__ == "__main__":

    print("NightCoder Target Finder")
    print("------------------------")

    target = input("Enter target text: ")

    print()
    print(f"Searching for: {target}")
    print()

    result = find_target(target)

    if result:
        print("Target found!")
        print()
        print(f'Text: {result["text"]}')
        print(f'Position: ({result["x"]}, {result["y"]})')
        print(f'OCR confidence: {result["confidence"]:.0f}%')
        print(f'Match similarity: {result["similarity"]:.2f}')

    else:
        print("Target not found.")

        