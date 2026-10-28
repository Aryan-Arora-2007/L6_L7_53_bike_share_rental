"""Lab 6 - Branch coverage tests for bike_share_rental.py

Goal: make every decision (if / elif) evaluate to BOTH True and False
(>= 90% branch coverage; this suite reaches 100%).

Run:
    coverage run --branch -m pytest BranchCoverageTest_bike_share_rental.py
    coverage report -m --include="bike_share_rental.py"
"""
import pytest
from bike_share_rental import ride_cost, dock_status, can_unlock


# ---------------------------------------------------------------- ride_cost
# Validation branches
def test_unknown_bike_type_raises():
    with pytest.raises(ValueError, match="unknown bike type"):
        ride_cost("scooter", 30, False, False)


@pytest.mark.parametrize("minutes", [0, -5])
def test_non_positive_duration_raises(minutes):
    with pytest.raises(ValueError, match="invalid duration"):
        ride_cost("standard", minutes, False, False)


def test_minimum_valid_duration_is_accepted():
    # minutes == 1 -> boundary just above the invalid range (False branch)
    assert ride_cost("standard", 1, False, False) == 20


# Block rounding
@pytest.mark.parametrize(
    "minutes, expected",
    [(30, 20), (31, 40), (45, 40), (60, 40)],
)
def test_block_rounding_standard(minutes, expected):
    assert ride_cost("standard", minutes, False, False) == expected


# Subscriber branches
def test_subscriber_single_block_is_free():
    # blocks -> 0 : `blocks <= 0` True
    assert ride_cost("standard", 20, True, False) == 0


def test_subscriber_free_even_when_peak():
    assert ride_cost("electric", 30, True, True) == 0


def test_subscriber_pays_after_first_block():
    # blocks 2 -> 1 : `blocks <= 0` False
    assert ride_cost("electric", 60, True, False) == 35


def test_non_subscriber_pays_all_blocks():
    assert ride_cost("cargo", 30, False, False) == 50


# Peak surcharge branches (is_peak and bike_type != "cargo")
def test_peak_surcharge_applied_standard():
    assert ride_cost("standard", 30, False, True) == 35


def test_peak_surcharge_applied_electric():
    assert ride_cost("electric", 30, False, True) == 50


def test_peak_no_surcharge_for_cargo():
    # is_peak True but bike_type == "cargo" -> condition False
    assert ride_cost("cargo", 30, False, True) == 50


def test_off_peak_no_surcharge():
    # is_peak False -> condition False
    assert ride_cost("standard", 30, False, False) == 20


# Long-ride fee branches (minutes > 180)
def test_exactly_180_minutes_no_long_fee():
    # 6 blocks * 20 = 120, no fee (boundary: not > 180)
    assert ride_cost("standard", 180, False, False) == 120


def test_181_minutes_long_fee_applies():
    # 7 blocks * 20 = 140 + 100 = 240
    assert ride_cost("standard", 181, False, False) == 240


def test_peak_and_long_ride_combined():
    # 200 min electric: 7*35 = 245 + 15 + 100 = 360
    assert ride_cost("electric", 200, False, True) == 360


def test_subscriber_long_ride_pays_fee():
    # 200 min standard sub: 7-1 = 6 blocks * 20 = 120 + 100 = 220
    assert ride_cost("standard", 200, True, False) == 220


# -------------------------------------------------------------- dock_status
@pytest.mark.parametrize("capacity", [0, -3])
def test_dock_invalid_capacity_raises(capacity):
    with pytest.raises(ValueError, match="invalid capacity"):
        dock_status(0, capacity)


def test_dock_negative_bikes_raises():
    with pytest.raises(ValueError, match="invalid bike count"):
        dock_status(-1, 10)


def test_dock_more_bikes_than_capacity_raises():
    with pytest.raises(ValueError, match="invalid bike count"):
        dock_status(11, 10)


def test_dock_empty():
    assert dock_status(0, 10) == "empty"


def test_dock_full():
    assert dock_status(10, 10) == "full"


def test_dock_few_bikes_one():
    assert dock_status(1, 10) == "few bikes"


def test_dock_few_bikes_boundary_two():
    assert dock_status(2, 10) == "few bikes"


def test_dock_just_above_few_bikes_is_available():
    # 3 bikes, 7 free -> neither few bikes nor few slots
    assert dock_status(3, 10) == "available"


def test_dock_few_slots_one_free():
    assert dock_status(9, 10) == "few slots"


def test_dock_few_slots_boundary_two_free():
    assert dock_status(8, 10) == "few slots"


def test_dock_just_below_few_slots_is_available():
    # 3 free slots
    assert dock_status(7, 10) == "available"


def test_dock_available_middle():
    assert dock_status(5, 10) == "available"


def test_dock_single_slot_capacity_full_and_empty():
    assert dock_status(0, 1) == "empty"
    assert dock_status(1, 1) == "full"


# --------------------------------------------------------------- can_unlock
def test_unlock_denied_when_active_ride():
    assert can_unlock(500, True, 30) is False


def test_unlock_denied_under_16():
    assert can_unlock(500, False, 15) is False


def test_unlock_age_16_enough_balance():
    assert can_unlock(100, False, 16) is True


def test_unlock_age_17_insufficient_balance():
    assert can_unlock(99, False, 17) is False


def test_unlock_age_18_boundary_uses_adult_rule():
    # 18 is not < 18 -> adult rule (>= 50)
    assert can_unlock(50, False, 18) is True


def test_unlock_adult_insufficient_balance():
    assert can_unlock(49, False, 40) is False


def test_unlock_adult_exact_balance():
    assert can_unlock(50, False, 30) is True
