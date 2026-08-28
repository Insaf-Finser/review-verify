import tempfile

from core.verify import verify_claim


def test_catches_false_clean_pass():
    # A command guaranteed to fail (nonexistent module)
    result = verify_claim("python -c \"import nonexistent_module_xyz\"", agent_claimed_passed=True)
    assert result.verified is False
    assert "did not run correctly" in result.reason


def test_confirms_real_pass():
    result = verify_claim("python -c \"print('ok')\"", agent_claimed_passed=True)
    assert result.verified is True

def test_no_tests_found_is_distinct_from_failure():
    # A real, empty directory with no test files collects zero tests,
    # which exits with code 5 — this should be flagged distinctly, not as a plain failure.
    with tempfile.TemporaryDirectory() as empty_dir:
        result = verify_claim(f"pytest {empty_dir}", agent_claimed_passed=True)
        assert result.verified is False
        assert "No tests were found" in result.reason