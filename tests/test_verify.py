from core.verify import verify_claim


def test_catches_false_clean_pass():
    # A command guaranteed to fail (nonexistent module)
    result = verify_claim("python -c \"import nonexistent_module_xyz\"", agent_claimed_passed=True)
    assert result.verified is False
    assert "did not run correctly" in result.reason


def test_confirms_real_pass():
    result = verify_claim("python -c \"print('ok')\"", agent_claimed_passed=True)
    assert result.verified is True