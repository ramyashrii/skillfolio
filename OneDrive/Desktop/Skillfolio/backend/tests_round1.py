from student_code import calculate_discount

def test_gold_tier():
    assert calculate_discount(100.0, "gold") == 80.0

def test_silver_tier():
    assert calculate_discount(100.0, "silver") == 90.0

def test_regular_tier():
    assert calculate_discount(100.0, "basic") == 100.0
