from app.core.negotiator import next_agent_offer


def test_no_auto_accept_under_margin():
    nxt = next_agent_offer(driver_price=1500, price_margin=2000, agent_price=1200, epsilon=1.0)
    assert nxt < 1500  # we counter below driver ask
    assert nxt > 1200  # move upward from our last offer


def test_accept_if_driver_below_agent():
    assert next_agent_offer(driver_price=1400, price_margin=2000, agent_price=1500) == 1400


def test_respect_cap_and_driver_minus_epsilon():
    nxt = next_agent_offer(driver_price=2300, price_margin=2000, agent_price=1500, epsilon=1.0)
    assert nxt <= 1999  # never at/above margin
    assert nxt < 2300  # never meets driver ask


def test_small_gap_nudges_but_stays_below_driver():
    nxt = next_agent_offer(driver_price=1700, price_margin=2000, agent_price=1690, min_step=50, epsilon=1.0)
    assert nxt == 1699  # driver-ask - epsilon

