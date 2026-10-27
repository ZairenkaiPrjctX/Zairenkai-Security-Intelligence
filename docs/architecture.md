# Architecture

`OSV-Scanner JSON -> normalize_osv -> versioned JSON report -> schema validation -> CI artifact` is the initial data path. The Python package has no runtime dependencies. The scanner process is invoked only by an explicit CLI command or scheduled workflow. CI uses read-only `GITHUB_TOKEN` permissions and scans the checked-out public repository.

App integration is not yet active: Zairenkai-App currently has no verified ZSI feed/client contract or report signing key. ZSC therefore displays Android build facts available to ordinary apps and accurately labels vulnerability/module assessment as not scanned/unknown. No device data is uploaded.
