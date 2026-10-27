# Threat model (initial)

| Threat | Current handling | Remaining limitation |
|---|---|---|
| Malformed report/JSON | JSON parser and required-field/status checks; schema validation in CI | Consumer-side validation not yet implemented in App |
| Forged or replayed report | Explicitly unsigned; consumers are told not to trust it | Signing, key rotation, freshness and replay protection are not implemented |
| Incorrect component/version match | Preserve scanner package identity and evidence path | OSV scanner scope does not cover device firmware, kernel backports or all vendor components |
| Supply-chain dependency | No Python runtime dependency; scanner must be installed separately from official release | Scanner binary provenance is not yet pinned by this repository |
| CI token leak | Read-only workflow permissions; no secrets required or printed | Organization-wide private repository credentials are not configured |
| False negatives / missing sources | Coverage is PARTIAL, with explicit limitations; absence of findings is not safe | Android, kernel, vendor and device feeds not implemented |
| Offline device / stale data | App has no remote-feed cache and ZSC shows unknown/not scanned | Feed freshness/cache UX follows after authenticated feed exists |
| Root unavailable / harmful remediation | ZSI and ZSC are read-only; no privileged operation is run | Device-specific integrity requires app/Core adapter and explicit permission model |
| Unnecessary device data transfer | No device data is uploaded | Future telemetry requires separate privacy review and user disclosure |
