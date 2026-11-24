from student_code import calculate_discount

def test_gold_with_promo():
    assert calculate_discount(100.0, "gold", is_promo=True) == 76.0

def test_silver_with_promo():
    assert calculate_discount(100.0, "silver", is_promo=True) == 85.5

def test_floor_cap():
    assert calculate_discount(100.0, "gold", is_promo=False) == 80.0
