import pytest
from app.asteroid_miner import process_mining_queue

def test_successful_mining():
    # Deposits: 10 (cost 25), 20 (cost 50). Total mined: 30. Total cost: 75.
    # Battery remaining: 100 - 75 = 25.
    assert process_mining_queue(100, 50, [10, 20]) == (30.0, 25.0, 0)

def test_insufficient_battery_skips():
    # Deposit 1: 20 (cost 50). Mined. Battery left: 50.
    # Deposit 2: 30 (cost 75). Skipped due to low battery.
    # Deposit 3: 10 (cost 25). Mined. Battery left: 25.
    assert process_mining_queue(100, 100, [20, 30, 10]) == (30.0, 25.0, 0)

def test_insufficient_cargo_skips():
    # Deposit 1: 30 (cost 75). Mined. Cargo left: 10.
    # Deposit 2: 20 (cost 50). Skipped due to low cargo space.
    # Deposit 3: 5 (cost 12.5). Mined. Cargo left: 5.
    assert process_mining_queue(200, 40, [30, 20, 5]) == (35.0, 112.5, 0)

def test_exact_capacity_boundaries():
    # Tests that students used >= rather than > for their checks.
    assert process_mining_queue(25, 10, [10]) == (10.0, 0.0, 0)

def test_float_deposit_values():
    # Ensures the programme correctly processes floating-point numbers.
    assert process_mining_queue(50.0, 20.0, [5.5]) == (5.5, 36.25, 0)

def test_zero_size_deposit():
    # A deposit of size 0 costs 0 battery and takes 0 cargo space.
    assert process_mining_queue(10, 10, [0]) == (0.0, 10.0, 0)

def test_corrupted_data_value_error():
    # "FLARE" cannot be converted to a float, triggering a ValueError.
    assert process_mining_queue(100, 50, [10, "FLARE", 10]) == (20.0, 50.0, 1)

def test_corrupted_data_type_error():
    # None and lists cannot be converted to a float, triggering a TypeError.
    scan = [None, [10, 20], 10]
    assert process_mining_queue(50, 50, scan) == (10.0, 25.0, 2)

def test_success_after_multiple_skips_and_errors():
    # Tests that the loop continues functioning after sequential failures.
    assert process_mining_queue(20, 50, [100, "ERROR", None, 5]) == (5.0, 7.5, 2)

def test_complex_scenario():
    # Initial: Battery 80, Cargo 30
    scan = [10, None, 20, "STATIC", 5]
    assert process_mining_queue(80, 30, scan) == (30.0, 5.0, 2)

def test_empty_queue():
    # An empty list should return initial values with zero mined and zero errors.
    assert process_mining_queue(100, 50, []) == (0, 100.0, 0)
