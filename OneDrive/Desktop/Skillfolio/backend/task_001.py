def calculate_discount(price: float, tier: str, is_promo: bool = False) -> float:
    """
    Nexora Tech Billing API (TASK-001)
    Round 1 Bug: 'gold' tier gives 20% off, 'silver' gives 10% off, others 0%.
    Currently the math adds the discount instead of subtracting it!
    """
    if price < 0:
        raise ValueError("Price cannot be negative")

    discount = 0.0
    if tier.lower() == "gold":
        discount = 0.20
    elif tier.lower() == "silver":
        discount = 0.10

    # BUG: Adding discount instead of subtracting
    final_price = price + (price * discount)
    return round(final_price, 2)
