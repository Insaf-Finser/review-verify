import subprocess


def test_cli_detects_mismatch():
    result = subprocess.run(
        ["review-verify", "run", "--check", "python -c \"exit(1)\"", "--claim", "all tests passed"],
        capture_output=True, text=True, check=False
    )
    assert result.returncode == 1
    assert "MISMATCH" in result.stdout