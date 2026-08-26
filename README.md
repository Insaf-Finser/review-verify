# review-verify

**Verify your AI agent actually ran the checks it says it ran — before you merge.**

AI coding agents are increasingly trusted to run tests, linters, and type-checks and report back
"all clear." But sometimes that report is wrong — not because the agent is lying, but because the
check silently failed to run at all (missing dependency, wrong environment, wrong interpreter).
`review-verify` re-runs the real check independently and catches the mismatch before a human merges
on false confidence.

## See it catch a real failure

This is an actual run from this project's own CI, no staged example:

```
Running: pytest
Real exit code: 127
Claimed passed: True
❌ MISMATCH — Agent claimed the check passed, but it actually failed or did not run correctly.

--- Real output ---
/bin/sh: 1: pytest: not found
```

The claim said "all tests passed." The environment didn't even have `pytest` installed. `review-verify`
caught it before it reached main.

## Status

🚧 Early development. Core verification logic, CLI, and GitHub Action all work end-to-end. Not yet
published to PyPI. Feedback and contributions welcome.

## Quickstart

**As a CLI, locally:**
```bash
pip install -e .
review-verify run --check "pytest" --claim "all tests passed"
```

**As a GitHub Action, automatically on every PR:**
```yaml
# .github/workflows/verify.yml
name: Verify AI Agent Claims
on: [pull_request]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -e ".[dev]"
      - uses: Insaf-Finser/review-verify/action@main
        with:
          check: "pytest"
          claim: "all tests passed"
```

## How it works

1. **Ground truth** — `review-verify` runs the real command itself and captures the actual exit code
   and output. No text-parsing guesswork on this side; exit codes are the same signal your shell
   already trusts.
2. **The claim** — either passed explicitly, or parsed from an agent's free-text summary
   (`core/parse.py`).
3. **The comparison** — a simple, auditable truth table: does the claim match reality? If not, the
   tool fails loudly with the real output attached, instead of letting a false "all clear" through.

## Why this exists

Right now, teams merge on trust in an agent's self-report. `review-verify` doesn't replace that trust
— it verifies it, the same way CI already re-runs tests instead of trusting a commit message that says
"tests pass."

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Good first issues are labeled `good-first-issue`.

## License

MIT