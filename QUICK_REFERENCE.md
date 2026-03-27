# DevTrace - Quick Reference Guide

## Command Cheat Sheet

### Setup & Configuration

```bash
# Initialize DevTrace in project
devtrace init

# Set up Jira credentials interactively
devtrace init jira
# Prompts: Host, Email, API Token

# Activate Git hooks
git config core.hooksPath .devtrace/hooks
```

---

## Phase 1: CLI Commands

### List Your Tickets

```bash
# Show all open tickets
devtrace tickets

# Filter by status
devtrace tickets list --status "In Progress"
devtrace tickets list -s "Done"

# Limit results
devtrace tickets list --limit 5
devtrace tickets list -l 10
```

### View Ticket Details

```bash
# Show full ticket info
devtrace tkt DT-21
devtrace tkt PROJ-456

# Hide comments
devtrace tkt DT-21 --no-comments
```

### Post Comments

```bash
# Comment on active ticket (from context)
devtrace comment "Fixed the bug!"

# Comment on specific ticket
devtrace comment "Ready for review" --ticket DT-25
devtrace comment "Approved" -t PROJ-456
```

### Manage Active Ticket

```bash
# Set active ticket
devtrace start DT-21

# Check active context
# (read from ~/.devtrace/configs/local/local_config.toml)
```

---

## Phase 2: Git Hooks (Automatic)

### What Happens Automatically

1. **Before you commit** (prepare-commit-msg)

   ```bash
   git commit -m "implement feature"
   # →  Message becomes: "DT-21 | FEAT : implement feature"
   ```

2. **While you commit** (commit-msg)

   ```bash
   # Validates format: [TICKET] | [TYPE] : [Description]
   # Fails if format is wrong
   ```

3. **After you commit** (post-commit)
   ```bash
   # Automatically posts:
   # 🤖 Automated DevTrace Update: Code committed
   # Commit: a3f8b2c
   # Files: +10, -2
   # To ticket: DT-21
   ```

### Manual Hook Triggers

```bash
# Manually trigger post-commit
devtrace hook post-commit

# Post commit even if marked [WIP]
devtrace hook post-commit --no-skip-wip

# Trigger prepare-commit-msg
devtrace hook prepare-commit-msg <file> message
```

### Bypass Hooks (If Needed)

```bash
# Skip all hooks for this commit
git commit --no-verify -m "message"

# Skip auto-comments: add [WIP] to message
git commit -m "[WIP] experimental - don't report"
```

---

## Configuration File

**Location**: `~/.devtrace/configs/local/local_config.toml`

### Structure

```toml
[jira]
host = "https://your-org.atlassian.net"
email = "your@example.com"
api_token = "ATATT3xFfGF0_xxxxx..."

[git]
github_token = "ghp_xxx..."
github_user = "username"

[active]
ticket_id = "DT-21"
started_at = "2026-02-21T18:44:05+05:30"
branch = "main"

[types]
allowed = ["FEAT", "FIX", "INIT", "DOCS", "REFACTOR", "TEST", "CHORE"]

[settings]
formater = true
```

### Getting Credentials

**Jira API Token**:

1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Name it "DevTrace" and copy the token
4. Use in `api_token` field

**GitHub Personal Access Token**:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scope: `repo` (full control of repositories)
4. Copy and use in `github_token` field

---

## Commit Message Format

### Standard Format

```
[TICKET-ID] | [TYPE] : [Description]
```

### Examples

```
DT-21 | FEAT : Implement Jira API integration
PROJ-456 | FIX : Resolve authentication timeout
DT-19 | DOCS : Update README with installation steps
```

### Allowed Types

| Type     | Meaning               | Example                              |
| -------- | --------------------- | ------------------------------------ |
| FEAT     | New feature           | FEAT : Add user authentication       |
| FIX      | Bug fix               | FIX : Resolve null pointer exception |
| INIT     | Initial setup         | INIT : Project scaffolding           |
| DOCS     | Documentation         | DOCS : Write API documentation       |
| REFACTOR | Code refactoring      | REFACTOR : Extract utility methods   |
| TEST     | Tests                 | TEST : Add unit tests for auth       |
| CHORE    | Build/CI/dependencies | CHORE : Update dependencies          |

---

## Common Workflows

### Daily Workflow

```bash
# Start of day: See what you need to work on
devtrace tickets

# Pick a ticket to work on
devtrace start DT-21

# During work: Make changes and commit
git add src/
git commit -m "add feature"
# → Auto-formatted to: DT-21 | FEAT : add feature
# → Auto-posted to Jira with commit details

# Check ticket progress
devtrace tkt DT-21

# When done: Post final comment
devtrace comment "Ready for code review"
```

### Multi-Ticket Day

```bash
# Start on ticket 1
devtrace start DT-21
git add src/
git commit -m "implement core logic"

# Switch to ticket 2
devtrace start DT-25
git add tests/
git commit -m "write unit tests"
# Future commits will auto-post to DT-25

# Switch back to ticket 1
devtrace start DT-21
git add docs/
git commit -m "add documentation"
# Future commits auto-post to DT-21 again
```

### Code Review Workflow

```bash
# Receive feedback on DT-21
devtrace tkt DT-21 --comments
# View recent comments/feedback

# Fix issues and commit
git add src/
git commit -m "address review feedback"

# Post update comment
devtrace comment "Review feedback incorporated, ready for re-review"
```

---

## Troubleshooting

### No Jira Credentials

**Error**: `Configuration Error: Missing Jira configuration keys: api_token`

**Solution**:

```bash
devtrace init jira
# Follow prompts to enter Host, Email, and API Token
```

### Hooks Not Running

**Check if activated**:

```bash
git config --get core.hooksPath
# Should output: .devtrace/hooks
```

**Re-activate**:

```bash
git config core.hooksPath .devtrace/hooks
```

### Commit Message Format Wrong

**Your message doesn't match format**:

```
DT-21 | FEAT : description  ✅ CORRECT
DT-21 description           ❌ WRONG (missing | TYPE :)
feat: description           ❌ WRONG (missing ticket ID)
```

**The `commit-msg` hook will reject it**. Correct the format and try again.

### Auto-Comments Not Posting

**Likely causes**:

1. No active ticket set → `devtrace start DT-21`
2. Jira API error → Check credentials with `devtrace init jira`
3. Network issue → Check Jira host is reachable
4. Message has `[WIP]` → Hooks skip WIP commits by design

**Debug**:

```bash
# Manually test post-commit
devtrace hook post-commit
# Should show success or error message
```

---

## Editor Integration (Coming Soon)

### VS Code

Once Phase 3 is ready, you'll be able to:

- View tickets in VS Code sidebar
- See associated commits inline
- Post comments from editor
- Switch active ticket from sidebar

### GitKraken

DevTrace hooks integrate with GitKraken's Git operations:

- Commit messages auto-formatted
- Hooks run transparently
- Comments posted without leaving GitKraken

---

## Performance Tips

### Large Repositories

For repos with many commits:

1. **Limit ticket fetching**:

   ```bash
   devtrace tickets list --limit 5
   ```

2. **Skip comment history** if slow:

   ```bash
   devtrace tkt DT-21 --no-comments
   ```

3. **Disable formatter** if hooks are slow:
   ```toml
   # In ~/.devtrace/configs/local/local_config.toml
   [settings]
   formater = false
   ```

---

## FAQ

### Q: What if I commit without setting an active ticket?

**A**: The `prepare-commit-msg` hook will note that no active ticket exists. You should run:

```bash
devtrace start DT-21
```

Then retry the commit.

---

### Q: Can I use DevTrace with multiple projects?

**A**: Yes! Each project has its own `.devtrace/` folder. Your **personal** credentials are stored in `~/.devtrace/configs/local/` (outside the project), so they're shared across all projects.

---

### Q: How secure are my credentials?

**A**:

- Credentials are stored in **local TOML file** (`~/.devtrace/configs/local/`)
- This folder is **git-ignored** automatically
- Credentials are **never** transmitted to DevTrace servers
- Only transmitted directly to Jira/GitHub APIs over HTTPS

**Recommendation**: Treat your API tokens like passwords. If compromised, revoke them immediately.

---

### Q: Can I use DevTrace with GitHub Issues instead of Jira?

**A**: Currently, DevTrace is Jira-focused. GitHub Issues support is planned for a future version.

---

### Q: What if I want to disable auto-comments for a commit?

**A**: Mark the commit as WIP:

```bash
git commit -m "[WIP] experimental feature - don't report"
# The post-commit hook will skip posting
```

---

### Q: Can the team see my auto-comments?

**A**: Yes! Auto-comments are posted to Jira tickets, so anyone with access to the ticket can see them. This is by design—keeping PMs informed.

---

## Keyboard Shortcuts (CLI)

There are no built-in keyboard shortcuts in the CLI, but you can create shell aliases:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias dt='devtrace'
alias dtt='devtrace tickets'
alias dts='devtrace start'
alias dtc='devtrace comment'

# Usage:
dt tickets
dts DT-21
dtc "Ready for review"
```

---

## Support

- **Documentation**: See `JIRA_INTEGRATION.md`, `GIT_HOOKS.md`, `PHASE_3_DASHBOARD.md`
- **Issues**: https://github.com/UtsavSingh315/devtrace-cli/issues
- **Discussions**: GitHub Discussions (coming soon)

---

## Version Info

```bash
devtrace version
# Outputs: DevTrace v0.1.0
```

---

## License

MIT License - See LICENSE file in repository
