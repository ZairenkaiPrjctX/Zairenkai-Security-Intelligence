"""Small, dependency-free OSV-Scanner report adapter and schema validator."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

SCHEMA = Path(__file__).resolve().parents[2] / "schemas" / "report-v1.schema.json"
STATUSES = {"AFFECTED", "FIXED", "NOT_AFFECTED", "POTENTIALLY_AFFECTED", "UNKNOWN", "NOT_SCANNED"}


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def normalize_osv(data: dict[str, Any], repository: str, commit: str, scanned_at: str | None = None) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    for result in data.get("results", []):
        source = result.get("source") or {}
        for package in result.get("packages", []):
            pkg = package.get("package") or {}
            for vuln in package.get("vulnerabilities", []):
                vuln_id = vuln.get("id")
                if not isinstance(vuln_id, str) or not vuln_id:
                    continue
                aliases = vuln.get("aliases") or []
                affected_ranges: list[dict[str, Any]] = []
                fixed_versions: set[str] = set()
                for affected in vuln.get("affected", []):
                    if not isinstance(affected, dict):
                        continue
                    for version_range in affected.get("ranges", []):
                        if not isinstance(version_range, dict):
                            continue
                        events = [
                            {kind: event[kind]}
                            for event in version_range.get("events", [])
                            for kind in ("introduced", "fixed", "last_affected")
                            if isinstance(event, dict) and isinstance(event.get(kind), str)
                        ]
                        affected_ranges.append({"type": str(version_range.get("type") or "UNKNOWN"), "events": events})
                        fixed_versions.update(event["fixed"] for event in events if "fixed" in event)
                findings.append({
                    "id": vuln_id,
                    "aliases": [a for a in aliases if isinstance(a, str)],
                    "repository": repository,
                    "commit": commit,
                    "component": {
                        "name": str(pkg.get("name") or "unknown"),
                        "version": str(pkg.get("version") or "unknown"),
                        "ecosystem": str(pkg.get("ecosystem") or "unknown"),
                    },
                    "status": "AFFECTED",
                    "affected_ranges": affected_ranges,
                    "severity": "UNKNOWN",
                    "severity_source": None,
                    "fixed_versions": sorted(fixed_versions),
                    "evidence": [{"source": "OSV-Scanner", "path": str(source.get("path") or "unknown"), "scanner_id": vuln_id}],
                    "references": [r["url"] for r in vuln.get("references", []) if isinstance(r, dict) and isinstance(r.get("url"), str)],
                    "confidence": "HIGH",
                    "mitigation": "Review the linked upstream advisory and update or mitigate according to that source.",
                })
    return {
        "schema_version": "1.0.0",
        "repository": repository,
        "commit": commit,
        "scan_status": "COMPLETED",
        "scanner": {"name": "OSV-Scanner", "version": str(data.get("version") or "unknown")},
        "scanned_at": scanned_at or _timestamp(),
        "sources": [{"name": "OSV-Scanner / OSV", "status": "AVAILABLE", "updated_at": None}],
        "coverage": {"status": "PARTIAL", "summary": "Dependency findings imported from OSV-Scanner output; device, kernel backports, vendor bulletins, and non-dependency code were not assessed."},
        "findings": findings,
        "limitations": ["No finding is not proof of safety.", "Kernel version and backport status are not evaluated.", "Severity remains unknown unless mapped from a supported scoring source."],
    }


def validate_report(report: dict[str, Any]) -> list[str]:
    """Validate JSON Schema constraints and safety-critical status invariants."""
    errors = [
        f"schema: {error.message} at {list(error.absolute_path)}"
        for error in Draft202012Validator(
            json.loads(SCHEMA.read_text(encoding="utf-8")), format_checker=FormatChecker()
        ).iter_errors(report)
    ]
    required = {"schema_version", "repository", "commit", "scan_status", "scanner", "scanned_at", "sources", "coverage", "findings", "limitations"}
    errors.extend(f"missing required field: {key}" for key in sorted(required - report.keys()))
    if report.get("schema_version") != "1.0.0":
        errors.append("unsupported schema_version")
    if report.get("scan_status") not in {"COMPLETED", "FAILED", "NOT_SCANNED"}:
        errors.append("invalid scan_status")
    if not isinstance(report.get("findings"), list):
        errors.append("findings must be an array")
    else:
        for i, finding in enumerate(report["findings"]):
            if not isinstance(finding, dict) or finding.get("status") not in STATUSES:
                errors.append(f"findings[{i}] has invalid status")
            elif finding.get("status") in {"FIXED", "NOT_AFFECTED"}:
                errors.append(f"findings[{i}] uses a verified status unsupported by this import adapter")
    return errors


def validate_schema_document() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != "https://zairenkaiprjctx.github.io/Zairenkai-Security-Intelligence/report-v1.schema.json":
        raise ValueError("report schema metadata mismatch")


def load_json(path: Path) -> dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError("JSON root must be an object")
    return obj
