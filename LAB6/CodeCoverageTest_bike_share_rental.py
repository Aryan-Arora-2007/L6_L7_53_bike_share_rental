"""Lab 6 - Code (line) coverage tests for bike_share_rental.py

Goal: execute every line of the application at least once (>= 90% line coverage).

Run:
    coverage run -m pytest CodeCoverageTest_bike_share_rental.py
    coverage report -m --include="bike_share_rental.py"
"""
import pytest
from bike_share_rental import ride_cost, dock_status, can_unlock


# ---------------------------------------------------------------- ride_cost
def test_standard_ride():
    # Starter example: 45 min -> 2 blocks * 20 = 40
    assert ride_cost("standard", 45, False, False) == 40


def test_unknown_bike_type_raises():
    with pytest.raises(ValueError, match="unknown bike type"):
        ride_cost("scooter", 30, False, False)


def test_invalid_duration_raises():
    with pytest.raises(ValueError, match="invalid duration"):
        ride_cost("standard", 0, False, False)


def test_subscriber_first_block_free():
    # 20 min -> 1 block, subscriber gets it free -> early return 0
    assert ride_cost("standard", 20, True, False) == 0


def test_subscriber_pays_remaining_blocks():
    # 60 min -> 2 blocks, 1 free, 1 paid at 35 = 35
    assert ride_cost("electric", 60, True, False) == 35


def test_peak_surcharge_and_long_ride_fee():
    # 200 min -> 7 blocks * 35 = 245, +15 peak, +100 long ride = 360
    assert ride_cost("electric", 200, False, True) == 360


# -------------------------------------------------------------- dock_status
def test_dock_invalid_capacity_raises():
    with pytest.raises(ValueError, match="invalid capacity"):
        dock_status(0, 0)


def test_dock_invalid_bike_count_raises():
    with pytest.raises(ValueError, match="invalid bike count"):
        dock_status(-1, 10)


def test_dock_empty():
    assert dock_status(0, 10) == "empty"


def test_dock_full():
    assert dock_status(10, 10) == "full"


def test_dock_few_bikes():
    assert dock_status(2, 10) == "few bikes"


def test_dock_few_slots():
    assert dock_status(8, 10) == "few slots"


def test_dock_available():
    assert dock_status(5, 10) == "available"


# --------------------------------------------------------------- can_unlock
def test_unlock_active_ride_denied():
    assert can_unlock(500, True, 30) is False


def test_unlock_under_16_denied():
    assert can_unlock(500, False, 15) is False


def test_unlock_teen_with_enough_balance():
    assert can_unlock(100, False, 17) is True


def test_unlock_adult_with_enough_balance():
    assert can_unlock(50, False, 30) is True
