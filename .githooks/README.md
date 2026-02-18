# Git Hooks

This directory contains custom git hooks for the project.

## Available Hooks

### pre-commit
- **Purpose**: Automatically format TypeScript code before each commit
- **Action**: Runs `npx prettier --write` on staged `.ts` files under `apps/` and `libs/`
- **Result**: Files are formatted and automatically re-added to staging

### pre-push
- **Purpose**: Verify code quality before pushing
- **Action**: Runs `npx prettier --check` and `npx eslint --max-warnings=0` on TypeScript sources
- **Result**: If formatting or lint checks fail, the push is cancelled with an error message

## Installation

To install the hooks in your local repository, run:

```bash
chmod +x .githooks/*
git config core.hooksPath .githooks
```

## Uninstall

To revert to Git's default hooks:

```bash
git config --unset core.hooksPath
```
