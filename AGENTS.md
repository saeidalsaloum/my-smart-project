# AGENTS.md

These instructions apply to the entire repository.

## Repository Mission

Maintain `my-smart-project` as a safe, minimal, reviewable foundation for future serious development. The repository should stay understandable to a human maintainer and to Codex. Do not turn it into a large application before the product scope is documented.

## Repository Scope

Allowed work:

- Small Python standard-library code changes.
- Tests that verify observable behavior.
- Documentation that clarifies scope, operation, security, or review process.
- Minimal repository configuration that improves local verification or CI.

Out of scope unless explicitly approved:

- Web frameworks, API servers, databases, authentication, deployment, analytics, payments, email, cloud infrastructure, AI SDKs, or external service integrations.
- Generated binary files or large assets.
- Legal, personal, private, media, analytics, or unrelated project materials.

## Forbidden Actions

Never:

- Add secrets, API keys, credentials, tokens, passwords, private data, or sensitive documents.
- Connect the project to external services.
- Add paid services or AI API integrations.
- Push directly to `main`.
- Merge a pull request.
- Delete files without first explaining why the deletion is safe and receiving explicit approval.
- Modify files outside this repository.
- Add broad architecture, large scaffolds, or fake placeholder features.

## Branch Rules

- Work on a review branch, not `main`.
- If an existing draft PR already contains the relevant work, update that branch instead of creating a duplicate.
- If a new branch is required, use a clear name beginning with `codex/`.
- Keep PRs draft until the human owner explicitly asks to mark them ready.
- Do not merge or delete branches unless explicitly instructed.

## Security Rules

- Treat `.env`, `.env.*`, key files, certificates, tokens, exported personal data, and private documents as forbidden repository content.
- Prefer documentation over implementation when security or privacy requirements are unclear.
- If a requested change could expose private data or connect to a service, stop and ask for confirmation.
- Do not invent credentials, example secrets, or real-looking tokens.

## Dependency Rules

- Use the Python standard library by default.
- Do not add third-party packages unless there is a documented need and explicit approval.
- If dependencies are added later, document why they are needed and how to install them.

## Testing Rules

Before reporting implementation as complete, run the smallest relevant verification commands when possible:

```bash
python3 -m src.main
python3 -m unittest discover -s tests
```

If a command cannot be run, report the exact reason. Do not present unrun checks as verified.

## Documentation Rules

Update documentation when changing behavior, commands, safety boundaries, scope, or workflow.

Primary documents:

- `README.md` for overview and quick start.
- `RUNBOOK.md` for local operation and troubleshooting.
- `docs/PROJECT_PLAN.md` for scope, phases, risks, and open decisions.
- `docs/DEVELOPMENT_GUIDE.md` for contribution workflow.
- `docs/SECURITY.md` for security and privacy rules.

## Review Requirements

Every completed change report must include:

- Files created and modified.
- Commands run and results.
- Security and privacy check.
- Dependency check.
- Whether `main` was modified.
- Remaining risks or uncertainties.
- Exact next human action.

## Escalation Behavior

When uncertain, choose the safest reversible path. If the uncertainty affects privacy, secrets, external services, data ownership, architecture, or deletion, stop and ask the human owner before changing files.
