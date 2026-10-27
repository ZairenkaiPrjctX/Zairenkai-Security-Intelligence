# Organization repository inventory and safe sync report

Inspected 2026-10-27 (UTC date). Organization list came from the public GitHub REST API `GET /orgs/ZairenkaiPrjctX/repos?per_page=100&type=all`; list was 17 repositories, all public and not archived at inspection. The unauthenticated result establishes public visibility only. `gh` is not installed; GitHub App repository list returned no entries, so private/restricted repositories cannot be ruled out. The target ZSI repository returned HTTP 404 and SSH `Repository not found`; creation permission is unavailable in this environment.

`git fetch --all --prune` succeeded for all 16 pre-existing local organization clones. Existing upstream-tracking branches were equal to fetched upstreams (0 ahead / 0 behind). The missing public organization repository `anime-extensions` was cloned with a shallow, blob-filtered clone and checked out at its API-reported default branch. No branch was reset or switched for sync. Dirty user files in App and Database Source were preserved. ZSI has only this local working directory and no remote.

| Repository | Default branch | Visibility / archived | Local clone / branch | Sync and worktree |
|---|---|---|---|---|
| Zairenkai-Graphics-Platform | dev | public / no | yes / dev | fetch OK; clean |
| Zairenkai-License-Server | dev | public / no | yes / dev | fetch OK; clean |
| Zairenkai-App | dev | public / no | yes / codex/central-release-feed | fetch OK; upstream equal before task; user patch files preserved; current ZSC work pending |
| Zairenkai-Intelligence-Engine | dev | public / no | yes / codex/ai-quality-and-resilience | fetch OK; upstream equal; clean |
| Zairenkai-Core | dev | public / no | yes / dev | fetch OK; upstream equal; clean |
| Zairenkai-Sdk | dev | public / no | yes / dev | fetch OK; upstream equal; clean |
| ZairenkaiPrjctX.github.io | dev | public / no | yes / dev | fetch OK; upstream equal; clean |
| Zairenkai-Database-Source | dev | public / no | yes / codex/database-source-ci-fix | fetch OK; upstream equal before task; user patch preserved; CI repair in progress |
| Zairenkai-FAS | dev | public / no | yes / dev | fetch OK; upstream equal; clean |
| Zairenkai-Release | dev | public / no | yes / codex/unified-matrix-builder | fetch OK; upstream equal; clean |
| .github | dev | public / no | yes / dev | fetch OK; upstream equal; clean |
| Zairenkai-ThermalTools | dev | public / no | yes / dev | fetch OK; upstream equal; clean |
| Zairenkai-ART | dev | public / no | yes / dev | fetch OK; upstream equal; clean |
| Zairenkai-Modules | dev | public / no | yes / codex/central-release-feed | fetch OK; upstream equal; clean |
| Zairenkai-Docs | dev | public / no | yes / dev | fetch OK; upstream equal; clean |
| anime-extensions | ccr-97bcb73d-9x6z9h | public / no | yes / ccr-97bcb73d-9x6z9h | shallow clone OK; separate product, excluded from Zairenkai integration |
| Zairenkai-Tuning | dev | public / no | yes / dev | fetch OK; upstream equal; clean |
| Zairenkai-Security-Intelligence | unavailable (404) | unavailable | local only / not initialized | remote missing or inaccessible; repository creation blocked |

## Access and next steps

- Local Git identity is configured. GitHub CLI is absent. GitHub App connection cannot list organization repositories and does not expose repository administration/secrets endpoints.
- Cannot create the ZSI GitHub repository, set its default branch/visibility, publish branches, configure GitHub environment `release`, or create/update GitHub Actions secrets with available interfaces.
- No secret values were read or output. The Release repository's existing project documentation records previously configured signing secrets, but current secret/environment state could not be queried through available permissions.
- Historical failed Actions were inspected once (not monitored): App run 40513651337 failed Kotlin compile at nullable routing in `integration-core/ai/Agent.kt`; its fix exists in the already-pushed App topic branch `codex/central-release-feed` (commit e9c546b). Database Source run 40513738489 failed Ruff E501 on `tools/export_app_candidates.py`; this task fixes those lines. Its full test suite additionally exposed stale workflow-name expectation for the existing `artifact-release.yml`; expectation was updated.
- No merge was attempted during organization sync because each fetched tracking branch was already equal. Task changes are isolated on topic branches.
