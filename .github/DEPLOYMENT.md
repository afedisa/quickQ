# GitHub Actions - Deployment (NestJS)

This repository deploys a NestJS application using GitHub Actions workflows built around Node.js and Docker.

## Current Workflows

### CI
- File: `.github/workflows/ci.yml`
- Triggers: `pull_request` and `push` to `develop`, `staging`, `master`, `main`
- Runs:
  - `npm ci`
  - `prettier --check`
  - `eslint`
  - `npm run build`
  - `npm run test -- --runInBand`
  - `npm audit --audit-level=high` (non-blocking)

### Deploy to Staging
- File: `.github/workflows/deploy-staging.yml`
- Trigger: `push` to `staging`
- Flow:
  1. Verifies quality (format/lint/build/test)
  2. Builds Docker image
  3. Triggers deployment webhook

### Deploy to Production
- File: `.github/workflows/deploy-production.yml`
- Trigger: `push` to `master` or `main`
- Flow:
  1. Verifies quality (format/lint/build/test/audit)
  2. Builds Docker image
  3. Triggers deployment webhook

### Docker Image
- File: `.github/workflows/docker-image.yml`
- Triggers: `pull_request` and `push` to `develop`, `staging`, `master`, `main`
- Flow:
  - Build image on PR
  - Build + push to GHCR on push

## Required Secrets

Configure in `Settings > Secrets and variables > Actions`:

```text
STAGING_DEPLOY_WEBHOOK
PRODUCTION_DEPLOY_WEBHOOK
```

Optional for notifications or integrations:

```text
SLACK_WEBHOOK
```

## Recommended Branch Strategy

- `develop`: continuous integration
- `staging`: automatic deployment to staging environment
- `master` / `main`: automatic deployment to production

## Local Verification Before Push

```bash
npm ci
npx prettier --check "apps/**/*.ts" "libs/**/*.ts"
npx eslint "{apps,libs}/**/*.ts" --max-warnings=0
npm run build
npm run test -- --runInBand
```

## Quick Troubleshooting

### Formatting/lint fails in CI
- Run `npm run format` and `npm run lint` locally.

### Build or tests fail
- Confirm local build with `npm run build`.
- Run tests with `npm run test -- --runInBand`.

### Staging/production does not deploy
- Verify webhook secret exists and URL is valid.
- Check logs of the `deploy` job in the Actions tab.

## Note

This documentation reflects the current project state (NestJS + npm + Docker + webhooks). If deployment mechanics change, update this file together with the workflows.
