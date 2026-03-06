"""
test_game_logic.py — Pytest cases for logic_utils.py

Tests target the two bugs that were fixed:
  1. Inverted hint messages in check_guess
  2. Incorrect difficulty range for Hard mode

Also includes tests for parse_guess and update_score.
"""

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


# ── check_guess tests ───────────────────────────────────────────────

def test_winning_guess():
    """If the guess equals the secret, outcome should be 'Win'."""
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


def test_guess_too_high():
    """If guess (60) > secret (50), outcome should be 'Too High'."""
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    """If guess (40) < secret (50), outcome should be 'Too Low'."""
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# ── BUG FIX VERIFICATION: Hint message direction ────────────────────

def test_too_high_message_says_lower():
    """BUG FIX: When guess is too high, the hint should tell the player
    to go LOWER (not HIGHER, which was the original broken behavior)."""
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    # The message must guide the player downward
    assert "LOWER" in message, f"Expected 'LOWER' in message, got: {message}"
    assert "HIGHER" not in message, f"Message should NOT say 'HIGHER': {message}"


def test_too_low_message_says_higher():
    """BUG FIX: When guess is too low, the hint should tell the player
    to go HIGHER (not LOWER, which was the original broken behavior)."""
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    # The message must guide the player upward
    assert "HIGHER" in message, f"Expected 'HIGHER' in message, got: {message}"
    assert "LOWER" not in message, f"Message should NOT say 'LOWER': {message}"


# ── BUG FIX VERIFICATION: Difficulty ranges ─────────────────────────

def test_hard_range_wider_than_normal():
    """BUG FIX: Hard mode must have a wider range than Normal so it is
    genuinely harder.  The original code had Hard = (1, 50) which was
    narrower than Normal = (1, 100)."""
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, (
        f"Hard upper bound ({hard_high}) should exceed Normal ({normal_high})"
    )


def test_easy_range_narrower_than_normal():
    """Easy mode should have a narrower range than Normal."""
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    assert easy_high < normal_high, (
        f"Easy upper bound ({easy_high}) should be less than Normal ({normal_high})"
    )


def test_all_ranges_start_at_one():
    """All difficulty levels should start at 1."""
    for level in ("Easy", "Normal", "Hard"):
        low, _ = get_range_for_difficulty(level)
        assert low == 1, f"{level} range should start at 1, got {low}"


# ── parse_guess tests ───────────────────────────────────────────────

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert "not a number" in err.lower()


def test_parse_decimal_truncates():
    """Decimal input like '42.7' should be accepted and truncated to 42."""
    ok, value, err = parse_guess("42.7")
    assert ok is True
    assert value == 42


# ── update_score tests ──────────────────────────────────────────────

def test_score_increases_on_win():
    new_score = update_score(0, "Win", 1)
    assert new_score > 0


def test_score_decreases_on_miss():
    new_score = update_score(100, "Too High", 1)
    assert new_score < 100


def test_win_bonus_decreases_with_attempts():
    """Winning on attempt 1 should give more points than winning on attempt 5."""
    score_early = update_score(0, "Win", 1)
    score_late = update_score(0, "Win", 5)
    assert score_early > score_late
