def next_agent_offer(
    driver_price: float,
    price_margin: float,
    agent_price: float,
    concede_rate: float = 0.5,   # how big each concession is toward target
    min_step: float = 50.0,      # minimum movement per round
    epsilon: float = 1.0,        # keeps us strictly below margin/driver ask
) -> float:
    """
    Compute the next agent offer with 'no auto-accept under margin' policy.

    Inputs:
      - driver_price: carrier's latest ask
      - price_margin: strict upper bound (final price must be < price_margin)
      - agent_price: agent's previous offer

    Returns:
      - next agent offer (float). If it equals driver_price, treat as acceptance upstream.
    """
    if price_margin <= 0:
        raise ValueError("price_margin must be > 0")
    if any(x < 0 for x in (driver_price, agent_price)):
        raise ValueError("prices must be >= 0")

    cap = price_margin - epsilon

    # If the driver undercuts (or matches) our last offer, accept that great deal.
    if driver_price <= agent_price:
        return float(driver_price)

    # Normal path: NEVER auto-accept just because driver is under the margin.
    # Set a target strictly below both the driver's ask and our hard cap.
    target = min(driver_price - epsilon, cap)

    # If target is at/below our last offer (e.g., tiny gap), nudge minimally but stay ≤ target.
    gap = target - agent_price
    if gap <= 0:
        # We were already at/above target; nudge up a hair but keep under target if possible.
        return float(min(agent_price + min_step, target))

    # Concede toward target, but stay below driver ask and below cap.
    step = max(min_step, gap * concede_rate)
    next_offer = agent_price + step

    # Clamp to target to ensure we don't meet/exceed the driver's ask or cap.
    return float(min(next_offer, target))


