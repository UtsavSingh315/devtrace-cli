# DevTrace Git Hook Integration - Phase 2

## Overview

Phase 2 automates Jira ticket updates without developer overhead. Git hooks automatically:

1. **Post commit details** to the active Jira ticket after every commit
2. **Prepend ticket IDs** to commit messages before the editor opens

This keeps Project Managers informed in real-time without manual effort.

---

## Setup

### Automatic Setup

When you run `devtrace init`, Git hooks are automatically created at `.devtrace/hooks/` and activated:

```bash
devtrace init
```

### Manual Activation

If hooks aren't activated, enable them with:

```bash
devtrace init hooks
```

This runs:

```bash
git config core.hooksPath .devtrace/hooks
```

---

## How It Works

### 1. Post-Commit Hook

**Trigger:** After every successful `git commit`

**Action:**

- Detects the currently active Jira ticket from `.devtrace/configs/local/local_config.toml`
- Extracts commit details: message, hash, files changed, diff stats
- Formats this as a comment and posts it to the Jira ticket
- Silently skips if no active ticket or if commit is marked `[WIP]`

**Example Auto-Comment:**

```
🤖 Automated DevTrace Update: Code committed

Commit Message:
FEAT: Implement Jira API integration

Commit Hash: a3f8b2c

Files Changed:
- src/devtrace/utils/jira_client.py (+145, -0)
- src/devtrace/commands/tickets.py (+89, -0)
- pyproject.toml (+2, -0)
```

### 2. Prepare-Commit-Msg Hook

**Trigger:** Before the commit message editor opens

**Action:**

- Pre-fills the commit message with the active ticket ID
- Format: `[TICKET-ID] | [Your message here]`
- Only activates for new commits (not merges, squashes, etc.)

**Example Flow:**

```bash
# Set active ticket
devtrace start DT-21

# Edit your files...
git add src/

# When you run git commit, the editor opens with:
# DT-21 |
# (cursor is ready for you to type)
```

---

## Commands

### `devtrace hook post-commit`

Manually trigger the post-commit hook outside of Git context.

**Usage:**

```bash
devtrace hook post-commit
devtrace hook post-commit --skip-wip  # Default behavior
devtrace hook post-commit --no-skip-wip  # Post even WIP commits
```

**Options:**

- `--skip-wip/--no-skip-wip`: Skip posting if commit message contains `[WIP]` (default: skip)

**Output Example:**

```
✅ Auto-comment posted to DT-21
Comment ID: 123456789012345
```

### `devtrace hook prepare-commit-msg`

Manually trigger the prepare-commit-msg hook.

**Usage:**

```bash
devtrace hook prepare-commit-msg /path/to/commit_editmsg message
```

**Note:** This is rarely needed manually—Git invokes it automatically.

---

## Configuration

### Hook Script Location

Hooks are stored in `.devtrace/hooks/`:

```
.devtrace/hooks/
├── post-commit          # Posts commit to Jira ticket
├── prepare-commit-msg   # Prepends ticket ID to message
└── commit-msg           # (Existing) Validates commit format
```

### Git Hook Configuration

Hooks are activated via Git config:

```bash
git config core.hooksPath .devtrace/hooks
```

Verify with:

```bash
git config --get core.hooksPath
```

---

## Behavior & Edge Cases

### When Post-Commit Hook Skips Silently

The hook will **not** post a comment in these cases (but commit still succeeds):

1. **No active ticket** — No ticket ID in context
2. **[WIP] in message** — Work in progress, not ready to report
3. **Jira API error** — Network issues, invalid credentials, etc.
4. **Configuration error** — Missing Jira credentials

**Why?** We never want Git operations to fail due to Jira API issues. The hook logs warnings but doesn't block commits.

### Disabling Auto-Comments

If you don't want auto-comments for a commit:

**Option 1:** Mark as WIP

```bash
git commit -m "[WIP] Experimental feature - don't report"
```

**Option 2:** Disable hook temporarily

```bash
git commit --no-verify -m "Bypass hooks"
```

**Option 3:** Clear active ticket

```bash
# Edit ~/.devtrace/configs/local/local_config.toml
# Set ticket_id = ""
```

---

## Commit Message Format

DevTrace enforces a standard commit format to ensure consistency.

### Format Rules

```
[TICKET-ID] | [TYPE]: [Description]
```

**Examples:**

```
DT-21 | FEAT: Implement Jira API integration
PROJ-456 | FIX: Resolve authentication timeout
DT-19 | DOCS: Update README with setup instructions
```

### Allowed Types

```
FEAT      - New feature
FIX       - Bug fix
INIT      - Initial commit / project setup
DOCS      - Documentation
REFACTOR  - Code refactoring (no functional change)
TEST      - Tests and test infrastructure
CHORE     - Build, CI/CD, dependency updates
```

### Validation

The `commit-msg` hook validates format before commit is finalized:

```bash
devtrace validate commit <commit_msg_file>
```

---

## Integration with Development Workflow

### Typical Development Flow

```bash
# 1. Start working on a ticket
devtrace start DT-21

# 2. Edit files and commit
git add src/
git commit -m "Implement core logic"
# Hook prepends: DT-21 | FEAT: Implement core logic
# Hook posts: Auto-comment to DT-21 with commit details

# 3. Continue development
git add tests/
git commit -m "Add unit tests"
# Auto-comments again to DT-21

# 4. View the ticket to see all updates
devtrace tkt DT-21
# Shows all auto-comments from your commits
```

### With Multiple Branches

```bash
# Feature branch
git checkout -b feature/DT-25
devtrace start DT-25

# Work and commit
git add src/
git commit -m "Implement feature"
# Auto-comment posts to DT-25

# Switch to another ticket
devtrace start DT-30
# Future commits will auto-comment to DT-30
```

---

## Troubleshooting

### Hooks Not Running

Check if hooks path is configured:

```bash
git config --get core.hooksPath
# Should output: .devtrace/hooks
```

If not set:

```bash
git config core.hooksPath .devtrace/hooks
```

### Manual Hook Execution

Test a hook manually:

```bash
# Test post-commit hook
devtrace hook post-commit

# Verify output appears in Jira ticket
devtrace tkt DT-21 --comments
```

### Debugging Hook Issues

Enable verbose output:

```bash
# Check hook file permissions
ls -la .devtrace/hooks/

# Manually run hook with error output
bash -x .devtrace/hooks/post-commit
```

### Hook Bypassing

If you need to bypass hooks temporarily:

```bash
git commit --no-verify -m "Your message"
```

---

## What's Next (Phase 3)

- **Phase 3**: React web dashboard with:
  - Unified Jira + Git data visualization
  - Kanban board view of tickets
  - Commit history per ticket
  - LOC metrics and time tracking
