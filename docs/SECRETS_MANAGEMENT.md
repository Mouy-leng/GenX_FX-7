# Secrets Management

NEVER commit real secrets. Use placeholders and store values in a secure manager.

## Storage Options
- GitHub Actions Secrets / Environments
- Local: `.env` (excluded) + a local secrets vault (e.g., 1Password, Bitwarden)
- Cloud: Provider secrets managers (e.g., AWS Secrets Manager, Azure Key Vault, GCP Secret Manager)

## Patterns
- Use `.env.example` with placeholders
- Load secrets at runtime via environment variables
- For GitHub App auth, store:
  - `GITHUB_APP_ID`
  - `GITHUB_APP_INSTALLATION_ID`
  - `GITHUB_APP_PRIVATE_KEY` (Base64-encoded if multiline)
  - `GITHUB_APP_WEBHOOK_SECRET`

## Rotation
- Maintain an inventory of secrets and owners
- Rotate on schedule or on compromise
- Version and timestamp secrets in manager; avoid sharing via chat/email

## Detection
- Enable secret scanning in GitHub
- Pre-commit hooks to prevent committing secrets


