def next_agent_offer(
    driver_price: float,
    price_margin: float,
    agent_price: float,
    concede_rate: float = 0.5,
    min_step: float = 50.0,
    epsilon: float = 1.0,
) -> float:
    """
    Pure function: compute the next agent offer.
    - Keeps final agreed price strictly below price_margin (by epsilon).
    - Returns driver_price when it's acceptable (treat as acceptance upstream).
    """
    if price_margin <= 0:
        raise ValueError("price_margin must be > 0")
    if any(x < 0 for x in (driver_price, agent_price)):
        raise ValueError("prices must be >= 0")

    cap = price_margin - epsilon
    # Accept immediately if driver ask is already acceptable.
    if driver_price <= cap:
        return float(driver_price)

    # Otherwise, move toward the cap/driver ask with a bounded concession.
    target = min(driver_price, cap)
    gap = target - agent_price
    # If no gap (or negative due to odd input), make a minimal nudge upward (but never exceed cap).
    if gap <= 0:
        return float(min(agent_price + min_step, cap))

    step = max(min_step, gap * concede_rate)
    return float(min(agent_price + step, cap))


