"""Command-line entry point."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from zsi.report import load_json, normalize_osv, validate_report, validate_schema_document


def write_report(report: dict, path: Path) -> None:
    errors = validate_report(report)
    if errors:
        raise ValueError("invalid report: " + "; ".join(errors))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(prog="zsi", description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="check schema and local configuration")
    imp = commands.add_parser("import-osv", help="normalize existing OSV-Scanner JSON output")
    imp.add_argument("input", type=Path)
    imp.add_argument("--repository", required=True)
    imp.add_argument("--commit", required=True)
    imp.add_argument("--output", type=Path, required=True)
    scan = commands.add_parser("scan", help="run installed osv-scanner on a repository")
    scan.add_argument("--repository", type=Path, default=Path("."))
    scan.add_argument("--commit", required=True)
    scan.add_argument("--output", type=Path, required=True)
    val = commands.add_parser("validate", help="validate a ZSI report")
    val.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "check":
            validate_schema_document()
            print("ZSI schema and local configuration: OK")
        elif args.command == "validate":
            errors = validate_report(load_json(args.input))
            if errors:
                print("\n".join(errors), file=sys.stderr)
                return 1
            print("report valid")
        else:
            if args.command == "scan":
                executable = shutil.which("osv-scanner")
                if not executable:
                    raise RuntimeError("osv-scanner is not installed; install a verified official release first")
                result = subprocess.run([executable, "scan", "--format", "json", str(args.repository)], check=False, capture_output=True, text=True)
                if result.returncode != 0:
                    raise RuntimeError(f"osv-scanner failed ({result.returncode}): {result.stderr.strip()}")
                data = json.loads(result.stdout)
            else:
                data = load_json(args.input)
            write_report(normalize_osv(data, args.repository.name if isinstance(args.repository, Path) else args.repository, args.commit), args.output)
            print(f"report written: {args.output}")
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"zsi: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
