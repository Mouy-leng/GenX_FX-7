# Secrets handling and secure storage

Do NOT commit real API keys, passwords, or credentials to the repository.

Recommendations:

- Store secrets in a local `.env` file that is listed in `.gitignore` (already added).
- Use a secret manager for production (Vault, AWS Secrets Manager, Azure Key Vault, or similar).
- If a secret was accidentally shared or committed, rotate it immediately and remove it from history.

Example local steps:

1. Create a local `.env` file from `.env.example`:

   cp .env.example .env

2. Populate `.env` with the real value locally (do NOT commit):

   CURSOR_API_KEY=key_...

3. If a key is exposed, rotate it in the provider dashboard and remove it from git history using BFG or git-filter-repo.
