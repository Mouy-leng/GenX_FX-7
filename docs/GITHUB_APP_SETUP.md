# GitHub App Registration and Owner Configuration

This guide documents creating a GitHub App, setting the repository owner, and installing the app for this workspace.

> Replace placeholders like `<ORG_OR_USER>` and `<APP_NAME>` with your values.

## 1) Decide Ownership Scope
- Organization-owned app (recommended for multi-repo): `<ORG_OR_USER>`
- User-owned app (single maintainer): `<GITHUB_USERNAME>`

Record the owner choice in `OWNERSHIP.md` and verify `.github/CODEOWNERS` reflects the desired teams/users.

## 2) Create the GitHub App
1. Navigate to Settings → Developer settings → GitHub Apps
2. Click “New GitHub App”
3. Fill basic details:
   - App name: `<APP_NAME>`
   - Homepage URL: `https://github.com/<ORG_OR_USER>`
   - Callback URL (if needed): your service URL or `https://example.com/callback`
   - Webhook URL: your webhook receiver URL (optional at creation)
   - Webhook secret: generate and store in secrets manager
4. Permissions (minimum principle of least privilege):
   - Repository permissions (example):
     - Contents: Read/Write (if pushing changes) or Read
     - Metadata: Read
     - Pull requests: Read/Write (if labeling/merging)
     - Issues: Read/Write (if labeling/commenting)
     - Actions: Read (or Read/Write if dispatching workflows)
   - Organization permissions (if needed): Members: Read
5. Subscribe to events as required (e.g., push, pull_request, issues)
6. Where can this GitHub App be installed?: Any account

## 3) Generate Credentials
- Create a Private key (PEM) and download securely
- Note the App ID and Installation ID
- If using OAuth for user-to-server, note Client ID and Client Secret

Store all credentials in your secrets manager and CI (e.g., GitHub Actions) as:
- `GITHUB_APP_ID`
- `GITHUB_APP_INSTALLATION_ID`
- `GITHUB_APP_PRIVATE_KEY` (PKCS#1 or PKCS#8, base64-encoded if needed)
- `GITHUB_APP_WEBHOOK_SECRET`

## 4) Install the App to the Owner and Repositories
1. Click “Install App” on the app page
2. Choose owner: `<ORG_OR_USER>` (or your username)
3. Select “Only select repositories” and pick this repo (and others as needed)

## 5) CI/CD Integration (GitHub Actions Example)
Use GitHub App auth to get a token for workflows.

```yaml
name: ci
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - name: Generate GitHub App token
        id: app-token
        uses: tibdex/github-app-token@v2
        with:
          app_id: ${{ secrets.GITHUB_APP_ID }}
          private_key: ${{ secrets.GITHUB_APP_PRIVATE_KEY }}
          installation_id: ${{ secrets.GITHUB_APP_INSTALLATION_ID }}
      - name: Use token
        run: |
          gh auth login --with-token <<< "${{ steps.app-token.outputs.token }}"
```

## 6) Webhook Receiver (Optional)
If your app processes webhooks, expose an HTTPS endpoint and verify the signature using `GITHUB_APP_WEBHOOK_SECRET`.

## 7) Governance and Audit
- Keep owners and teams updated in `OWNERSHIP.md` and `.github/CODEOWNERS`
- Enforce branch protection and required reviews for owner teams
- Rotate app private keys per your security policy

## 8) Troubleshooting
- 401/403 from API: verify app permissions and token scope
- App not appearing on PRs: ensure installation on the correct owner and repo access
- Signature mismatch: check webhook secret and HMAC algorithm (SHA-256)


