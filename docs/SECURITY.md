# Security and Privacy

`my-smart-project` must not contain secrets, credentials, private data, sensitive documents, or unrelated personal material.

## Do Not Commit

Never commit:

- API keys, tokens, passwords, credentials, or certificates.
- `.env` or `.env.*` files with real values.
- Private personal data.
- Legal documents or case material.
- Media files, analytics exports, or unrelated project archives.
- Real customer, user, financial, or identity data.

## Current Security Posture

The current project:

- Uses only the Python standard library.
- Requires no secrets.
- Connects to no external services.
- Has no deployment configuration.
- Stores no application data.

## If Sensitive Data Is Found

1. Stop work immediately.
2. Do not copy, summarize, or spread the sensitive content.
3. Notify the human owner with the file path and a brief description of the risk.
4. Wait for explicit instructions before making cleanup changes.

## Dependency and Service Changes

Before adding dependencies, external services, paid tools, AI APIs, deployment configuration, or data storage, document the reason and get explicit approval.
