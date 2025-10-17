from app.core.negotiator import next_agent_offer


def test_accept_when_under_cap():
    assert next_agent_offer(1500, 1600, 1200) == 1500  # accept driver


def test_concede_toward_cap_but_not_over():
    nxt = next_agent_offer(driver_price=2200, price_margin=2000, agent_price=1500)
    assert nxt <= 1999  # strict below price_margin
    assert nxt > 1500  # moves upward


def test_min_step_when_gap_small():
    nxt = next_agent_offer(driver_price=1700, price_margin=2000, agent_price=1680, min_step=50)
    assert nxt >= 1730  # at least min_step from 1680, but <= 1999

