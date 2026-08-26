from core.parse import parse_agent_claim


def test_detects_clear_success():
    assert parse_agent_claim("All tests passed. Ready to merge.") is True


def test_detects_clear_failure():
    assert parse_agent_claim("2 tests failed, please review.") is False


def test_detects_negated_success():
    assert parse_agent_claim("Not all tests passed in this run.") is False


def test_returns_none_when_unclear():
    assert parse_agent_claim("I made some changes to the auth module.") is None