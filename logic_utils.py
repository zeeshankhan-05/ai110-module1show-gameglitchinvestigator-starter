"""
logic_utils.py — Pure game logic, separated from Streamlit UI.

Contains functions for difficulty ranges, input parsing,
guess evaluation, and score calculation.
"""


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty.

    Easy  → 1–50   (small pool, forgiving)
    Normal → 1–100  (standard)
    Hard  → 1–500  (large pool, challenging)
    """
    if difficulty == "Easy":
        return 1, 50
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # FIX: Was (1, 50) — narrower than Normal, making Hard easier.
        # Now (1, 500) so Hard is genuinely harder.
        # COLLAB: Identified via AI-assisted code review; refactored into
        # logic_utils.py using Copilot Agent mode, verified with pytest.
        return 1, 500
    # Fallback to Normal range for any unrecognized difficulty
    return 1, 100


def parse_guess(raw: str):
    """Parse user input into an integer guess.

    Returns:
        (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        # Handle decimal input by converting to float first, then int
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except (ValueError, TypeError):
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """Compare guess to secret and return (outcome, message).

    outcome is one of: "Win", "Too High", "Too Low"
    message is a user-friendly hint string.
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        # FIX: Message was "Go HIGHER!" which is the opposite of what the
        # player should do.  Now correctly says "Go LOWER!"
        # COLLAB: AI spotted the inverted hints; refactored into logic_utils.py
        # using Copilot Agent mode and confirmed with targeted pytest cases.
        return "Too High", "📉 Too high — go LOWER!"
    else:
        # FIX: Message was "Go LOWER!" which is the opposite of what the
        # player should do.  Now correctly says "Go HIGHER!"
        return "Too Low", "📈 Too low — go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update and return the new score based on outcome and attempt number.

    Win  → bonus points that shrink with each attempt (min 10).
    Miss → small penalty of –5 points.
    """
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    # Any incorrect guess costs 5 points
    return current_score - 5
