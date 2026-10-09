import pyautogui
from explorer_reader import read_explorer
from difflib import SequenceMatcher
from pathlib import Path


# ============================================================
# SETTINGS
# ============================================================

FILE_EXTENSIONS = (
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

SIMILARITY_THRESHOLD = 0.70
CONFIDENCE_THRESHOLD = 40

EXPLORER_MAX_X = 350
MIN_Y = 90
MAX_Y = 700


# ============================================================
# SIMILARITY
# ============================================================

def similarity(a, b):
    return SequenceMatcher(
        None,
        a.lower(),
        b.lower()
    ).ratio()


# ============================================================
# NORMALIZE
# ============================================================

def normalize_filename(text):
    text = text.strip().lower()
    text = text.replace("|", "")
    text = text.replace("\\", "")
    text = text.replace(" ", "")
    return text


# ============================================================
# FILE HELPERS
# ============================================================

def get_extension(filename):
    return Path(
        normalize_filename(filename)
    ).suffix.lower()


def get_base_name(filename):
    return Path(
        normalize_filename(filename)
    ).stem.lower()


def same_extension(target, candidate):

    target_extension = get_extension(target)
    candidate_extension = get_extension(candidate)

    if not target_extension:
        return True

    return target_extension == candidate_extension


def exact_filename_match(target, candidate):

    return (
        normalize_filename(target)
        ==
        normalize_filename(candidate)
    )


def base_name_similarity(target, candidate):

    target_base = get_base_name(target)
    candidate_base = get_base_name(candidate)

    if not target_base or not candidate_base:
        return 0.0

    return similarity(
        target_base,
        candidate_base
    )


# ============================================================
# FIND CANDIDATES
# ============================================================

def find_explorer_candidates(target, screen_results):

    candidates = []

    normalized_target = normalize_filename(target)

    for item in screen_results:

        text = item["text"].strip()

        if not text:
            continue

        x = item["x"]
        y = item["y"]
        confidence = item["confidence"]

        # ----------------------------------------------------
        # Explorer safety boundaries
        # ----------------------------------------------------

        if x > EXPLORER_MAX_X:
            continue

        if y < MIN_Y:
            continue

        if y > MAX_Y:
            continue

        normalized_text = normalize_filename(text)

        candidate_extension = get_extension(
            normalized_text
        )

        # Must be a supported file.
        if candidate_extension not in FILE_EXTENSIONS:
            continue

        # ----------------------------------------------------
        # Exact match
        # ----------------------------------------------------

        if exact_filename_match(
            normalized_target,
            normalized_text
        ):

            candidates.append({
                "text": text,
                "normalized_text": normalized_text,
                "x": x,
                "y": y,
                "confidence": confidence,
                "similarity": 1.0,
                "base_similarity": 1.0,
                "match_type": "exact",
                "pass": item.get(
                    "pass",
                    "unknown"
                ),
            })

            continue

        # ----------------------------------------------------
        # Fuzzy matching
        #
        # Extension must still match.
        # ----------------------------------------------------

        if not same_extension(
            target,
            normalized_text
        ):
            continue

        filename_score = similarity(
            normalized_target,
            normalized_text
        )

        base_score = base_name_similarity(
            target,
            normalized_text
        )

        if (
            filename_score >= SIMILARITY_THRESHOLD
            and
            base_score >= 0.75
            and
            confidence >= CONFIDENCE_THRESHOLD
        ):

            candidates.append({
                "text": text,
                "normalized_text": normalized_text,
                "x": x,
                "y": y,
                "confidence": confidence,
                "similarity": filename_score,
                "base_similarity": base_score,
                "match_type": "fuzzy",
                "pass": item.get(
                    "pass",
                    "unknown"
                ),
            })

    return candidates


# ============================================================
# DEDUPLICATE CANDIDATES
# ============================================================

def deduplicate_candidates(candidates):

    groups = {}

    for candidate in candidates:

        key = (
            candidate["normalized_text"],
            candidate["x"],
            candidate["y"],
        )

        if key not in groups:
            groups[key] = []

        groups[key].append(candidate)

    final_candidates = []

    for group in groups.values():

        # Highest confidence result wins.
        best = max(
            group,
            key=lambda item: (
                item["match_type"] == "exact",
                item["confidence"],
                item["similarity"],
                item["base_similarity"],
            )
        )

        # Record how many OCR passes agreed.
        best["ocr_pass_count"] = len(group)

        # Keep all OCR pass names for debugging.
        best["ocr_passes"] = sorted(
            {
                item.get(
                    "pass",
                    "unknown"
                )
                for item in group
            }
        )

        final_candidates.append(best)

    return final_candidates


# ============================================================
# FIND TARGET
# ============================================================

def find_target(target):

    print()
    print(
        f"Scanning Explorer for: {target}"
    )

    # --------------------------------------------------------
    # One multi-pass OCR capture
    # --------------------------------------------------------

    screen_results = read_explorer()

    candidates = find_explorer_candidates(
        target,
        screen_results
    )

    # --------------------------------------------------------
    # Remove duplicate results from different OCR passes
    # --------------------------------------------------------

    candidates = deduplicate_candidates(
        candidates
    )

    if not candidates:
        return None

    # --------------------------------------------------------
    # Sort strongest candidate first
    # --------------------------------------------------------

    candidates.sort(
        key=lambda item: (
            item["match_type"] == "exact",
            item["confidence"],
            item["similarity"],
            item["base_similarity"],
            item["ocr_pass_count"],
        ),
        reverse=True
    )

    # --------------------------------------------------------
    # Safety check for competing fuzzy candidates
    # --------------------------------------------------------

    if len(candidates) >= 2:

        first = candidates[0]
        second = candidates[1]

        if (
            first["match_type"] != "exact"
            and
            second["match_type"] != "exact"
        ):

            score_difference = (
                first["similarity"]
                -
                second["similarity"]
            )

            same_position = (
                abs(
                    first["x"] -
                    second["x"]
                ) <= 10
                and
                abs(
                    first["y"] -
                    second["y"]
                ) <= 10
            )

            if (
                not same_position
                and
                score_difference < 0.05
            ):

                print(
                    "⚠️ Multiple similar "
                    "targets detected."
                )

                print(
                    "NightCoder will NOT guess."
                )

                return None

    return candidates[0]


# ============================================================
# TEST MODE
# ============================================================

if __name__ == "__main__":

    print()
    print(
        "NightCoder Explorer Target Finder"
    )
    print(
        "---------------------------------"
    )
    print()

    target = input(
        "Enter file to find: "
    ).strip()

    print()

    print(
        f"Searching Explorer for: {target}"
    )

    screen_results = read_explorer()

    candidates = find_explorer_candidates(
        target,
        screen_results
    )

    candidates = deduplicate_candidates(
        candidates
    )

    print()
    print(
        f"Safe Explorer candidates: "
        f"{len(candidates)}"
    )

    print()

    for i, candidate in enumerate(
        candidates,
        start=1
    ):

        passes = ", ".join(
            candidate["ocr_passes"]
        )

        print(
            f"{i}. "
            f'{candidate["text"]} '
            f'-> '
            f'{candidate["normalized_text"]} '
            f'position='
            f'({candidate["x"]}, '
            f'{candidate["y"]}) '
            f'filename_similarity='
            f'{candidate["similarity"]:.2f} '
            f'base_similarity='
            f'{candidate["base_similarity"]:.2f} '
            f'confidence='
            f'{candidate["confidence"]:.0f}% '
            f'passes='
            f'{candidate["ocr_pass_count"]} '
            f'[{passes}] '
            f'type='
            f'{candidate["match_type"]}'
        )

    print()

    if not candidates:

        print(
            "❌ No safe Explorer target found."
        )

        print(
            "NightCoder will NOT click anything."
        )

    else:

        result = candidates[0]

        print(
            "SELECTED TARGET"
        )

        print(
            "----------------"
        )

        print(
            f'Text: {result["text"]}'
        )

        print(
            f'Normalized: '
            f'{result["normalized_text"]}'
        )

        print(
            f'Position: '
            f'({result["x"]}, '
            f'{result["y"]})'
        )

        print(
            f'Filename similarity: '
            f'{result["similarity"]:.2f}'
        )

        print(
            f'Base similarity: '
            f'{result["base_similarity"]:.2f}'
        )

        print(
            f'Confidence: '
            f'{result["confidence"]:.0f}%'
        )

        print(
            f'OCR passes agreeing: '
            f'{result["ocr_pass_count"]}'
        )

        print(
            f'OCR passes: '
            f'{", ".join(result["ocr_passes"])}'
        )

        print(
            f'Match type: '
            f'{result["match_type"]}'
        )