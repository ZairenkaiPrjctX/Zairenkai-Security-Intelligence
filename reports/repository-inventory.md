# Organization repository inventory and safe sync report

Inspected 2026-10-27 (UTC date). The first public GitHub REST inventory returned 17 repositories, all public and not archived. A follow-up inventory after the maintainer created ZSI returned 18 repositories, all public and not archived. The unauthenticated API establishes public visibility only; private/restricted repositories cannot be ruled out. `gh` is now installed but `gh auth status` reports that it is not logged in. GitHub App repository listing and administration/secrets APIs are unavailable through the connected integration.

`git fetch --all --prune` succeeded for all 16 pre-existing local organization clones. Existing upstream-tracking branches were equal to fetched upstreams (0 ahead / 0 behind). The missing public organization repository `anime-extensions` was cloned with a shallow, blob-filtered clone and checked out at its API-reported default branch. ZSI was initially empty with API default branch `main`; its local work was pushed to branch `dev`, tracking `origin/dev`. The GitHub default branch remains `main`. No branch was reset or force-pushed. Dirty user patch files in App and Database Source were preserved.

| Repository | Default branch | Visibility / archived | Local clone / branch | Sync and worktree |
|---|---|---|---|---|
| Zairenkai-Graphics-Platform | dev | public / no | yes / dev | fetch OK; clean |
| Zairenkai-License-Server | dev | public / no | yes / dev | fetch OK; clean |
| Zairenkai-App | dev | public / no | yes / codex/central-release-feed | commits pushed; UI work in branch; user patch files preserved; draft PR blocked by API 403 |
| Zairenkai-Intelligence-Engine | dev | public / no | yes / codex/ai-quality-and-resilience | fetch OK; upstream equal; clean |
| Zairenkai-Core | dev | public / no | yes / dev | fetch OK; upstream equal; clean |
| Zairenkai-Sdk | dev | public / no | yes / dev | fetch OK; upstream equal; clean |
| ZairenkaiPrjctX.github.io | dev | public / no | yes / dev | fetch OK; upstream equal; clean |
| Zairenkai-Database-Source | dev | public / no | yes / codex/database-source-ci-fix | CI fix commit pushed; user patch preserved; draft PR blocked by API 403 |
| Zairenkai-FAS | dev | public / no | yes / dev | fetch OK; upstream equal; clean |
| Zairenkai-Release | dev | public / no | yes / codex/unified-matrix-builder | invalid download-artifact pin corrected and pushed |
| .github | dev | public / no | yes / dev | fetch OK; upstream equal; clean |
| Zairenkai-ThermalTools | dev | public / no | yes / dev | fetch OK; upstream equal; clean |
| Zairenkai-ART | dev | public / no | yes / dev | fetch OK; upstream equal; clean |
| Zairenkai-Modules | dev | public / no | yes / codex/fix-release-update-url-assertion | release URL assertion corrected and branch pushed |
| Zairenkai-Docs | dev | public / no | yes / dev | fetch OK; upstream equal; clean |
| anime-extensions | ccr-97bcb73d-9x6z9h | public / no | yes / ccr-97bcb73d-9x6z9h | shallow clone OK; separate product, excluded from Zairenkai integration |
| Zairenkai-Tuning | dev | public / no | yes / dev | fetch OK; upstream equal; clean |
| Zairenkai-Security-Intelligence | main (GitHub default) | public / no | yes / dev tracking origin/dev | initial repository content was pushed; default branch was not changed |

## Access and next steps

- Local Git identity is configured. GitHub CLI 2.103.3 is installed, but has no authenticated session. Draft PR creation via the connected GitHub integration returned HTTP 403.
- Environment and Actions secrets cannot be read or updated until `gh auth login` is completed with a credential permitted to administer `Zairenkai-Release`. Secret values must not be sent in chat or committed.
- A local RSA-4096 JKS keystore was generated and keytool-validated at `/root/.config/zairenkai/release-signing/` with mode 0600. It has not been pushed; private signing keys must only enter GitHub via encrypted Actions secrets after the account is authenticated and the key identity is confirmed.
- Current failed run logs inspected (completed runs only; no ongoing run monitoring): App run 40524526295 failed compilation of `AiUiTest.kt` due to missing `onFirst` import; fixed in pushed App branch commit 44a01bf. Release run 40524130180 failed to resolve a mistyped `actions/download-artifact` SHA; corrected in pushed Release commit 9c54e0a using the official v8.0.2 commit. Modules run 40524442444 failed a release URL assertion that omitted the actual `module-` tag prefix; corrected in pushed Modules commit 30ca4fe. Database Source run 40513738489 had Ruff E501 and a stale workflow-name test; both are fixed in pushed Database Source commit c7614b6.
- No merge was attempted during organization sync because each fetched tracking branch was already equal. Task changes are isolated on topic branches.
