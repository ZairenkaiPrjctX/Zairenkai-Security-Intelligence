# Zairenkai Security Intelligence (ZSI)

ZSI normalizes vulnerability findings from explicit scanner outputs into a versioned report. The initial adapter imports the official OSV-Scanner JSON output; it does not claim that unscanned repositories or devices are safe. Android/vendor/kernel bulletin feeds and signed release-feed delivery are not implemented yet.

## Requirements and use

Python 3.11 or newer and the pinned `jsonschema` dependency. Install OSV-Scanner separately using its official installation instructions and verify its published release/checksum. Then run:

```sh
python -m zsi.cli check
python -m zsi.cli scan --repository . --commit "$(git rev-parse HEAD)" --output report.json
python -m zsi.cli import-osv osv-results.json --repository Zairenkai-App --commit <sha> --output report.json
python -m zsi.cli validate report.json
```

`scan` invokes the installed `osv-scanner scan --format json` and fails clearly if the executable is absent or exits unsuccessfully. `import-osv` normalizes an existing scanner result. JSON output follows `schemas/report-v1.schema.json`; validation checks JSON Schema Draft 2020-12. A detected scanner finding is `AFFECTED`; packages without findings and repositories not scanned are not labeled safe. Scope and confidence limitations are carried into every report.

## Status and scope

The schema separates repository scan status from finding status. Finding statuses include AFFECTED, FIXED, NOT_AFFECTED, POTENTIALLY_AFFECTED, UNKNOWN, and NOT_SCANNED. The current adapter can establish AFFECTED only from OSV-Scanner findings. Other classifications remain unavailable until there is evidence and a source adapter. Kernel version alone is never treated as proof because backports are not mapped.

## CI and credentials

Pull request and push CI runs unit tests and schema validation without secrets. The scheduled workflow scans only this checkout, and produces an artifact; it does not access private organization repositories or publish security claims. Organization-wide access, publication to Zairenkai-Release, provenance/signing, and a verified report feed require separately provisioned least-privilege credentials and are not configured here. Never put credentials in this repository or send them in chat.

## Development

```sh
python -m pip install -r requirements.txt
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m zsi.cli check
```

See `docs/architecture.md`, `docs/threat-model.md`, and `docs/integration-contract.md` for boundaries and known limitations.
