import re


def parse_agent_claim(agent_text: str) -> bool | None:
    """
    Extract a pass/fail claim from an agent's summary text.
    Returns True if the agent claims success, False if it claims failure,
    None if no clear claim could be found (caller should handle this case
    explicitly rather than assuming pass or fail).
    """
    text = agent_text.lower()

    # Order matters: check failure signals first, since agents sometimes
    # write "not all tests passed" or "tests failed" which could otherwise
    # false-match a naive "passed" search.
    failure_patterns = [
        r"tests? failed",
        r"checks? failed",
        r"\bfailed\b",
        r"did not pass",
        r"not all .* passed",
    ]
    for pattern in failure_patterns:
        if re.search(pattern, text):
            return False

    success_patterns = [
        r"all tests? passed",
        r"tests? passed",
        r"checks? passed",
        r"\ball checks? (are )?green\b",
        r"\bsuccess(ful)?\b",
    ]
    for pattern in success_patterns:
        if re.search(pattern, text):
            return True

    return None