from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import ConfigError, load_spec
from .report import write_json_report, write_markdown_report
from .run import run_spec


def _run_command(args: argparse.Namespace) -> int:
    try:
        spec = load_spec(args.spec)
    except ConfigError as exc:
        print(f"AgentSpec config error: {exc}", file=sys.stderr)
        return 2

    report = run_spec(spec)
    md_path = Path(args.report)
    json_path = Path(args.json_report) if args.json_report else md_path.with_suffix(".json")
    write_markdown_report(report, md_path)
    write_json_report(report, json_path)

    print(f"AgentSpec: {report.status}")
    print(f"Agent: {report.agent_name}")
    print(f"Cases: {report.total_cases} | Passed: {report.passed_cases} | Failed: {report.failed_cases}")
    print(f"Average score: {report.average_score}/100")
    print(f"Markdown report: {md_path}")
    print(f"JSON report: {json_path}")

    if report.failed_cases:
        print("\nFailures:")
        for result in report.results:
            if not result.passed:
                print(f"- {result.case_id}: {len(result.failures)} failed checks")
                for check in result.failures[:3]:
                    print(f"  • {check.name}: {check.detail}")

    return 0 if report.status == "PASS" or args.no_fail else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentspec",
        description="Run contract tests against an AI agent command.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run an AgentSpec YAML file.")
    run.add_argument("spec", help="Path to agentspec.yaml")
    run.add_argument("--report", default="reports/agentspec-report.md", help="Markdown report output path")
    run.add_argument("--json-report", default=None, help="JSON report output path")
    run.add_argument("--no-fail", action="store_true", help="Always exit 0, useful for demos showing failing agents.")
    run.set_defaults(func=_run_command)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
