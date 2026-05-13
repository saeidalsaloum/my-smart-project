# Branch Hygiene Plan

## Audit Context

- Audit date: 2026-05-13.
- Main commit inspected: `bb10c682e26540377775e49d2156ef40caf4e403`.
- Scope: remote branches under `origin`, local branch awareness, and merged PR branch mapping.
- Result: no branches were deleted.

## Classification Method

Branches were classified from local Git branch inspection, remote head inspection,
merged-PR metadata, and ancestry checks against the inspected main commit.

- `KEEP`: active, protected, unknown, or not safe to classify for cleanup.
- `AUDIT RETAIN`: merged or historically useful branch that should be kept until a later explicit cleanup approval.
- `SAFE CLEANUP CANDIDATE`: branch associated with a merged PR and suitable for deletion only after a separate explicit approval.
- `UNKNOWN`: branch with insufficient evidence for classification.

Squash-merged PR branches may not appear as direct Git ancestors of `main` even
when their PR content is present on `main`. Before deleting any branch, confirm
the PR is merged and the branch still points to the expected reviewed head.

## KEEP

- `origin/main` at `bb10c682e26540377775e49d2156ef40caf4e403`.

## AUDIT RETAIN

- `origin/codex/minimal-starter` at `e276d2c155bba3c23359421f2f52f21e5ad18c2d`.
  PR #1 is merged, but this remote branch head was not confirmed as a direct
  ancestor of the inspected main commit during this audit.

## SAFE CLEANUP CANDIDATES

These branches should only be deleted in a future branch-cleanup task with
explicit approval:

- `origin/codex/content-command-center-v1` at `5e1db5a64d14316b30c5e3e5b37a0c0b579d4a2f` for merged PR #2.
- `origin/codex/content-command-center-v3-section-status-editing` at `57e0ebf87551928035749dafa91d8881e6da18a9` for merged PR #4.
- `origin/codex/content-command-center-v3c-section-status-hardening` at `3ffabebdd5e50336de7f317190c89d09389b5b2b` for merged PR #5.
- `origin/codex/content-command-center-v3d-stored-section-status-validation` at `98e1a659b39506122f3d63f9d7121558dc6bec1c` for merged PR #6.
- `origin/codex/content-command-center-v3e-export-brief-metadata-statuses` at `aa9847c4af8bc61507101f186ae49abdb41434e2` for merged PR #7.
- `origin/codex/content-command-center-v3f-project-overview-ux` at `cc3fb3e6b582c6337e8229b7adff6202ca11c637` for merged PR #8.
- `origin/codex/content-command-center-v3g-next-small-improvement` at `b8064c3ef43c65f41488a133beee643001ce207f` for merged PR #9.
- `origin/codex/content-command-center-v3h-next-small-improvement` at `6bcb29a1ffd58b878fa04d07f8a1fffe1c392cd5` for merged PR #10.
- `origin/codex/content-command-center-v3i-docs-consistency-audit` at `63b0f52a70ba40885f9d76e15332c2cdb592f80d` for merged PR #11.
- `origin/codex/content-command-center-v3j-branch-hygiene-plan` at `6245809ada0d13f7f1b1bf7e2feac2811d1e8219` for merged PR #12.

## UNKNOWN

- None from the available PR mapping. Retained branches with uncertainty are
  listed under `AUDIT RETAIN`.

## Future Cleanup Warning

No cleanup was performed in this plan. Deleting branches is a separate
destructive repository-maintenance action and requires explicit future approval.

If deletion is later approved, use this template one branch at a time:

```bash
git push origin --delete <branch-name>
```

Do not run that command until a future task explicitly authorizes branch
deletion for the named branch.

## Risks Of Deleting Too Early

- Losing quick access to reviewed branch tips for post-merge audits.
- Deleting a branch whose remote head changed after its PR was merged.
- Confusing squash-merge history with direct Git ancestry.
- Removing context that is still useful for release-traceability checks.
- Accidentally deleting an active or protected branch if the branch name is copied incorrectly.

## Manual Confirmation Checklist

Before any future cleanup:

- Confirm the branch name exactly.
- Confirm the associated PR number.
- Confirm the PR state is merged.
- Confirm the branch is not open, active, protected, or needed for an audit.
- Confirm the branch head is still the expected reviewed commit.
- Confirm no branch deletion command is bundled with unrelated changes.
- Delete one branch at a time and verify the result before continuing.
