# Repository Ownership and Governance

Primary owner: `<ORG_OR_USER>`

## Roles
- Platform Admins: `@<ORG_OR_USER>/platform-admins`
- Project Maintainers: `@<ORG_OR_USER>/projects-maintainers`
- Tools Maintainers: `@<ORG_OR_USER>/tools-maintainers`
- Trading Maintainers: `@<ORG_OR_USER>/trading-maintainers`

## Responsibilities
- Approvals: As configured in `.github/CODEOWNERS` and branch protection
- Incident Response: Platform Admins
- Secret Management: Platform Admins with least-privilege access

## Change Control
- Use PRs with required reviews from respective code owners
- Tag the relevant team per folder scope
- Use semantic commit messages (e.g., feat:, fix:, chore:)

## Escalation
1. Ping the relevant team in the PR
2. Escalate to Platform Admins
3. Ownership changes require a PR updating this file and `CODEOWNERS`


