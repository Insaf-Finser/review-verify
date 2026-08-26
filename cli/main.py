import argparse
import sys

from core.verify import verify_claim_from_text

def main():
    parser = argparse.ArgumentParser(
        prog="review-verify",
        description="Verify that an AI agent's claimed check results match reality.",
    )

    subparsers = parser.add_subparsers(dest="command",required=True)

    run_parser = subparsers.add_parser("run",help="Run a check and verify a claim against it")
    run_parser.add_argument("--check", required=True, help='Command to run, e.g. "pytest"')
    run_parser.add_argument("--claim", required=True, help="Agent's claim text, e.g. \"all tests passed\"")

    args = parser.parse_args()

    if args.command == "run":
        result = verify_claim_from_text(args.check, args.claim)

        print(f"Running: {result.command}")
        print(f"Real exit code: {result.real_exit_code}")
        print(f"Claimed passed: {result.claimed_passed}")

        if result.verified:
            print("✅ VERIFIED — claim matches reality")
            sys.exit(0)
        else:
            print(f"❌ MISMATCH — {result.reason}")
            print("\n--- Real output ---")
            print(result.real_output)
            sys.exit(1)


if __name__ == "__main__":
    main()