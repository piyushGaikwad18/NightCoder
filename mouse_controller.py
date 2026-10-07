import math
import random
import time

import pyautogui


# --------------------------------------------------
# NightCoder Mouse Controller
# --------------------------------------------------

def smooth_move_to(target_x, target_y, duration=None):
    """
    Move the mouse from its current position to the target
    using a fast, smooth, shallow curved path.
    """

    # Current mouse position
    start_x, start_y = pyautogui.position()

    # Difference between start and target
    dx = target_x - start_x
    dy = target_y - start_y

    # Total distance
    distance = math.hypot(dx, dy)

    # Already at target
    if distance < 5:
        return

    # --------------------------------------------------
    # Movement speed
    # --------------------------------------------------

    if duration is None:
        duration = max(
            0.05,
            min(0.25, distance / 4500)
        )

    # --------------------------------------------------
    # Direction perpendicular to start → target
    # --------------------------------------------------

    perpendicular_x = -dy / distance
    perpendicular_y = dx / distance

    # --------------------------------------------------
    # Very shallow U-shaped arc
    # Similar to the curve you showed.
    # --------------------------------------------------

    arc_height = distance * random.uniform(0.08, 0.12)

    # Curve can go either side
    direction = random.choice([-1, 1])

    # Number of movement points
    steps = max(
        10,
        min(25, int(distance / 35))
    )

    start_time = time.perf_counter()

    # --------------------------------------------------
    # Move along the curved path
    # --------------------------------------------------

    for i in range(steps + 1):

        progress = i / steps

        # Smooth acceleration / deceleration
        t = progress * progress * (
            3 - 2 * progress
        )

        # Straight-line base position
        base_x = start_x + dx * t
        base_y = start_y + dy * t

        # Shallow U-shaped arc
        arc = (
            4
            * arc_height
            * t
            * (1 - t)
        )

        # Final position on curved path
        x = (
            base_x
            + perpendicular_x
            * arc
            * direction
        )

        y = (
            base_y
            + perpendicular_y
            * arc
            * direction
        )

        # Move cursor
        pyautogui.moveTo(
            round(x),
            round(y),
            duration=0
        )

        # Precise timing
        target_time = (
            start_time
            + duration * progress
        )

        remaining = (
            target_time
            - time.perf_counter()
        )

        if remaining > 0:
            time.sleep(remaining)

    # --------------------------------------------------
    # Guarantee exact final position
    # --------------------------------------------------

    pyautogui.moveTo(
        target_x,
        target_y,
        duration=0
    )


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    print("--------------------------------")
    print("     NightCoder Mouse Test")
    print("--------------------------------")
    print()
    print("Move your mouse to a safe position.")
    print("Starting in 3 seconds...")

    time.sleep(3)

    print("Moving...")

    # Test destination
    smooth_move_to(1000, 700)

    print("Movement complete.")