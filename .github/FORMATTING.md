# Code Formatting and Quality Gates

This NestJS project uses local Git hooks and CI checks to enforce consistent formatting and code quality before push and merge.

## Local Hooks

### pre-commit
- Location: `.githooks/pre-commit`
- Action: formats staged TypeScript files (`apps/**` and `libs/**`) with Prettier.
- Result: formatted files are automatically re-added to staging.

### pre-push
- Location: `.githooks/pre-push`
- Action: runs formatting and lint validation:
  - `npx prettier --check "apps/**/*.ts" "libs/**/*.ts"`
  - `npx eslint "{apps,libs}/**/*.ts" --max-warnings=0`
- Result: blocks push if checks fail.

## GitHub Actions CI

Workflow: `.github/workflows/ci.yml`

Checks run on `pull_request` and `push` to `develop`, `staging`, `master`, and `main`:
- `npm ci`
- `prettier --check`
- `eslint`
- `npm run build`
- `npm run test -- --runInBand`
- `npm audit --audit-level=high` (informational, non-blocking)

## Hook Setup

```bash
chmod +x .githooks/*
git config core.hooksPath .githooks
```

## Recommended Workflow

```bash
# 1) Format (optional, pre-commit already formats staged files)
npm run format

# 2) Run lint
npm run lint

# 3) Run tests
npm run test -- --runInBand

# 4) Commit and push
git add .
git commit -m "feat: changes"
git push
```

## If pre-push fails

```bash
npm run format
npm run lint
git add .
git commit -m "style: fix format/lint"
git push
```

## Temporarily disable hooks

```bash
git config --unset core.hooksPath
# or for a single commit
git commit --no-verify -m "message"
```

> Note: even if local hooks are disabled, GitHub CI still validates formatting and lint.
