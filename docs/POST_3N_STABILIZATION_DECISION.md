# Post-3N Stabilization Decision

## Decision Context

- Decision date: 2026-05-13.
- Main commit inspected: `dbbfd16c0ae365366fdcbe278c6131bb5d9ce282`.
- Scope: current CLI behavior, documentation alignment, test stability, test maintainability, and branch hygiene posture after Phase 3N.
- Result: preserve stability and avoid new implementation by default.

## Current Product State

The project remains a local, public-safe Python CLI for generic video production project records. It uses the Python standard library and local JSON files in user-selected workspaces.

Current commands:

- `status`
- `init-workspace`
- `new-video`
- `list-videos`
- `overview-videos`
- `show-video`
- `update-status`
- `update-field`
- `update-section-status`
- `export-brief`

No new command behavior, schema, workflow, dependency, packaging, or integration change was introduced by Phase 3M or Phase 3N.

## Test-Governance Status

Phase 3M added deterministic coverage proving `overview-videos` remains read-only and does not rewrite workspace files.

Phase 3N added a small test-local `_read_project` helper and applied it to a limited set of repeated project JSON reads. The helper is scoped to `tests/test_main.py` and does not affect production behavior.

The test suite remains stable at 34 tests. `tests/test_main.py` is large, but still manageable. Further helperization should wait for a new decision gate and should remain test-only unless a separate mission explicitly authorizes production-code work.

## Documentation Status

README, RUNBOOK, `docs/PROJECT_PLAN.md`, `docs/BRANCH_HYGIENE_PLAN.md`, and `docs/STRATEGIC_STABILIZATION_AUDIT.md` remain aligned with the current command surface and safety model.

This checkpoint records that the earlier strategic stabilization recommendation has now been followed by two test-quality phases. The resulting posture is still stabilization-first.

## Branch Hygiene Status

Branch cleanup remains planning-only. No branch deletion was performed by this decision.

Any future branch cleanup requires a separate explicit deletion mission and must reconfirm each branch name, associated PR, merge state, and head SHA immediately before deletion.

## Stabilization Decision

The safest next move is to stop implementation by default.

Recommended posture:

- Prefer read-only audits and release gates over new feature work.
- Avoid broad test refactors while the suite is stable.
- Keep any future test cleanup tiny, deterministic, and scoped.
- Preserve the current JSON schema and CLI command semantics.
- Keep branch cleanup separate from feature, docs, or test work.

## Acceptable Future Work

Only after a new decision gate:

- Read-only stabilization or release audit.
- Tiny test-only helperization if it clearly reduces duplication without changing behavior.
- Docs-only correction if concrete drift appears.
- CLI UX planning without implementation by default.
- Separately approved branch cleanup planning or deletion mission.

## Must Not Change Without Explicit Approval

- Stored JSON schema.
- Existing CLI command semantics.
- Production code behavior.
- GitHub workflows.
- Dependencies.
- Packaging.
- Repository settings or branch protection.
- Secrets, credentials, tokens, environment variables, private settings, or media.
- Branch deletion.
- External integrations.
