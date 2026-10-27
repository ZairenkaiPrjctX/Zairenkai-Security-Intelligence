# Integration contract (draft v1)

The report JSON Schema at `schemas/report-v1.schema.json` is the sole current wire contract. Consumers must reject an unsupported `schema_version`, validate every required field, enforce a freshness policy using `scanned_at`, and preserve `scan_status` separately from finding status. Reports are unsigned in this initial version and must not be treated as authenticated or delivered to users as trusted security state. The App has no consumer yet. Adding distribution requires a reviewed signing format, key lifecycle, replay/freshness policy and tests before App integration.

Each finding binds repository and commit to component name/version/ecosystem, status, evidence, references, confidence, and mitigation. UNKNOWN and NOT_SCANNED are not aliases for safe. Severity is UNKNOWN unless a supported source is mapped. The initial OSV adapter marks only scanner-reported advisories AFFECTED.
