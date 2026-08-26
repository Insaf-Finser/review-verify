import subprocess
from dataclasses import dataclass

from core.parse import parse_agent_claim


@dataclass
class VerificationResult:
    command: str
    real_exit_code: int
    real_output: str
    claimed_passed: bool
    verified: bool
    reason: str


def run_real_check(command: str) -> tuple[int, str]:
    """Actually run the check command and capture real exit code + output."""
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, check=False
    )
    output = result.stdout + result.stderr
    return result.returncode, output


def verify_claim(command: str, agent_claimed_passed: bool) -> VerificationResult:
    """Compare what really happened against what the agent claimed happened."""
    real_exit_code, real_output = run_real_check(command)
    really_passed = real_exit_code == 0

    if agent_claimed_passed and not really_passed:
        return VerificationResult(
            command=command,
            real_exit_code=real_exit_code,
            real_output=real_output,
            claimed_passed=agent_claimed_passed,
            verified=False,
            reason="Agent claimed the check passed, but it actually failed or did not run correctly.",
        )

    return VerificationResult(
        command=command,
        real_exit_code=real_exit_code,
        real_output=real_output,
        claimed_passed=agent_claimed_passed,
        verified=really_passed == agent_claimed_passed,
        reason="Claim matches real result." if really_passed == agent_claimed_passed
               else "Agent claimed failure, but the check actually passed.",
    )

def verify_claim_from_text(command: str, agent_text: str) -> VerificationResult:
    claimed = parse_agent_claim(agent_text)
    if claimed is None:
        real_exit_code, real_output = run_real_check(command)
        return VerificationResult(
            command=command,
            real_exit_code=real_exit_code,
            real_output=real_output,
            claimed_passed=False,
            verified=False,
            reason="Could not determine a clear pass/fail claim from agent text — flagging for manual review.",
        )
    return verify_claim(command, claimed)