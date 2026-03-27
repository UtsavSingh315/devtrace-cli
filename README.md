# DevTrace 🚀

> **Seamless Jira ↔ Git bridge CLI**: Auto-format commits, keep PMs informed without browser hell.

DevTrace eliminates context-switching between Git, Jira, and browsers by integrating ticket and commit data into a unified CLI and (coming soon) web dashboard.

```bash
# Start working on a ticket
devtrace start DT-21

# Make changes and commit (hooks auto-format + auto-post)
git add src/
git commit -m "implement feature"

# Check your progress
devtrace tkt DT-21

# View all your tickets
devtrace tickets
```

---

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/UtsavSingh315/devtrace-cli
cd devtrace-cli
uv sync
```

### 2. Configure Jira Credentials

```bash
devtrace init jira
# Prompts for: Host, Email, API Token
# Get API Token: https://id.atlassian.com/manage-profile/security/api-tokens
```

### 3. Activate Git Hooks (Automatic)

```bash
devtrace init
# Creates .devtrace/ folder and activates hooks
```

### 4. Start Using DevTrace

```bash
# Set active ticket
devtrace start DT-21

# View your tickets
devtrace tickets

# View specific ticket
devtrace tkt DT-21

# Post a comment
devtrace comment "Working on this now"

# Commit (hooks handle the rest)
git add .
git commit -m "implement feature"
# → Auto-formatted: DT-21 | FEAT : implement feature
# → Auto-posted to Jira: 🤖 Automated DevTrace Update
```

---

## Features

### Phase 1: CLI Jira Integration ✅

#### `devtrace tickets` - List Your Tickets

```bash
devtrace tickets                              # All open tickets
devtrace tickets list --status "In Progress"  # Filter by status
devtrace tickets list --limit 5               # Limit results
```

**Output**: Rich table with ticket ID, summary, status, dates, and links.

#### `devtrace tkt <id>` - View Ticket Details

```bash
devtrace tkt DT-21                # Full ticket view
devtrace tkt DT-21 --no-comments  # Hide comments
```

**Output**: Panel with summary, description, assignee, status, and recent comments.

#### `devtrace comment "message"` - Post Comments

```bash
devtrace comment "Ready for review"           # Post to active ticket
devtrace comment "Looks good!" --ticket DT-25 # Post to specific ticket
```

**Features**: Detects active ticket from context, posts directly to Jira.

### Phase 2: Git Hook Automation ✅

#### Automatic Commit Formatting

```bash
git commit -m "implement api"
# Hook transforms to: DT-21 | FEAT : implement api
```

#### Automatic Jira Comments

```bash
# After commit, hook auto-posts:
# 🤖 Automated DevTrace Update: Code committed
# Commit Hash: a3f8b2c
# Files Changed: +45, -3
# → Posted to DT-21
```

#### Commit Message Validation

Only accepts format: `[TICKET-ID] | [TYPE] : [Description]`

### Phase 3: React Dashboard 🚀 (Coming Soon)

- **God-View Dashboard**: Unified Jira + Git data
- **Kanban Board**: Tickets organized by status
- **Metrics**: LOC changes, files modified, time tracking
- **Commit History**: See all commits associated with a ticket

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     DevTrace Ecosystem                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  CLI (Python)          Git Hooks           Dashboard        │
│  ─────────────         ──────────          ────────────     │
│  • tickets list        • Auto-format       • React 18+      │
│  • tkt <id>           • Validation        • Kanban board    │
│  • comment "msg"      • Auto-post to      • LOC metrics     │
│  • init               Jira                 • Time tracking   │
│  • start <ticket>                                           │
│                                                             │
│              ↓ All use ↓                                    │
│      ~/.devtrace/configs/local/local_config.toml           │
│      • Jira Host, Email, API Token                         │
│      • GitHub Token (for dashboard)                        │
│      • Active Ticket Context                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Configuration

### Setup Credentials

```bash
devtrace init jira
# Creates: ~/.devtrace/configs/local/local_config.toml
```

### Config File

Location: `~/.devtrace/configs/local/local_config.toml`

```toml
[jira]
host = "https://your-org.atlassian.net"
email = "your@example.com"
api_token = "ATATT3xFfGF0_..."

[git]
github_token = "ghp_..."
github_user = "username"

[active]
ticket_id = "DT-21"
branch = "main"
started_at = "2026-02-21T18:44:05+05:30"
```

### Getting Credentials

**Jira API Token**:

1. https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Copy and paste into config

**GitHub Token** (for Phase 3 dashboard):

1. https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scope: `repo`
4. Copy and paste into config

---

## Commit Message Format

DevTrace enforces a standard commit format:

```
[TICKET-ID] | [TYPE] : [Description]
```

### Examples

```
DT-21 | FEAT : Implement Jira API integration
PROJ-456 | FIX : Resolve authentication timeout
DT-19 | DOCS : Update README with setup instructions
DT-20 | TEST : Add unit tests for auth module
```

### Allowed Types

- **FEAT** - New feature
- **FIX** - Bug fix
- **INIT** - Initial setup / project scaffold
- **DOCS** - Documentation
- **REFACTOR** - Code refactoring (no functional change)
- **TEST** - Tests and test infrastructure
- **CHORE** - Build, CI/CD, dependencies

---

## Workflows

### Daily Development

```bash
# 1. See what you need to work on
devtrace tickets

# 2. Pick a ticket and set it active
devtrace start DT-21

# 3. Make changes and commit
git add src/
git commit -m "implement feature"
# → Hook auto-formats and posts to Jira

# 4. Check progress
devtrace tkt DT-21

# 5. Post updates when needed
devtrace comment "Ready for code review"
```

### Multi-Ticket Day

```bash
# Switch between tickets
devtrace start DT-21    # Work on DT-21
git commit -m "msg"     # Auto-posts to DT-21

devtrace start DT-25    # Switch to DT-25
git commit -m "msg"     # Auto-posts to DT-25
```

---

## Troubleshooting

### Q: Jira credentials not found?

```bash
devtrace init jira
# Follow the prompts
```

### Q: Hooks not running?

```bash
git config --get core.hooksPath
# Should output: .devtrace/hooks

# If not, re-activate:
git config core.hooksPath .devtrace/hooks
```

### Q: Commit message format wrong?

Format must be: `[TICKET] | [TYPE] : [Description]`

```
✅ DT-21 | FEAT : implement api
❌ DT-21 implement api (missing | TYPE :)
❌ feat: implement api (missing ticket ID)
```

### Q: Auto-comments not posting?

Likely causes:

1. No active ticket set → `devtrace start DT-21`
2. Invalid Jira credentials → `devtrace init jira`
3. Commit marked `[WIP]` → Hooks skip WIP by design
4. Network/API error → Check Jira host is reachable

---

## Documentation

- **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** - Command cheat sheet & FAQs
- **[JIRA_INTEGRATION.md](./JIRA_INTEGRATION.md)** - Phase 1 detailed guide
- **[GIT_HOOKS.md](./GIT_HOOKS.md)** - Phase 2 detailed guide
- **[PHASE_3_DASHBOARD.md](./PHASE_3_DASHBOARD.md)** - Phase 3 architecture
- **[PROJECT_STATUS.md](./PROJECT_STATUS.md)** - Implementation status report
- **[IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)** - Complete overview

---

## Project Status

### Phase 1: CLI Jira Integration ✅ COMPLETE

- ✅ `devtrace tickets` - Fetch and display tickets
- ✅ `devtrace tkt` - View ticket details
- ✅ `devtrace comment` - Post comments
- ✅ Config management (TOML parser)
- ✅ Error handling

### Phase 2: Git Hook Automation ✅ COMPLETE

- ✅ Auto-format commit messages
- ✅ Validate commit format
- ✅ Auto-post commits to Jira
- ✅ Graceful error handling

### Phase 3: React Dashboard 🚀 ARCHITECTED

- 🚀 Onboarding/Setup view
- 🚀 Kanban board of tickets
- 🚀 Enriched with commit data
- 🚀 Metrics visualization
- 🚀 Time tracking

---

## Installation

### Prerequisites

- Python 3.13+
- Git
- Jira account with API token access

### Install DevTrace

```bash
# Clone the repository
git clone https://github.com/UtsavSingh315/devtrace-cli
cd devtrace-cli

# Install dependencies
uv sync

# Verify installation
uv run devtrace --help
```

### Add to PATH (Optional)

```bash
# On Windows (PowerShell)
[Environment]::SetEnvironmentVariable("PATH", "$env:PATH;C:\Users\YourUsername\Desktop\devtrace-cli", "User")

# On macOS/Linux
echo 'export PATH="/path/to/devtrace-cli:$PATH"' >> ~/.bashrc
```

---

## Tech Stack

### CLI (Implemented)

- **Python 3.13** - Core language
- **Typer** - CLI framework
- **Rich** - Terminal UI / tables
- **TOML** - Configuration parsing
- **Jira** - Jira API client
- **GitPython** - Git integration

### Dashboard (Planned)

- **React 18+** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **react-beautiful-dnd** - Kanban board

---

## Development

### Project Structure

```
devtrace-cli/
├── src/devtrace/
│   ├── main.py                    # Entry point
│   ├── commands/                  # CLI commands
│   │   ├── tickets.py            # devtrace tickets
│   │   ├── tkt.py                # devtrace tkt
│   │   ├── comment.py            # devtrace comment
│   │   ├── hook.py               # Git hooks
│   │   └── ...
│   └── utils/                     # Utilities
│       ├── config.py             # TOML config
│       └── jira_client.py        # Jira API wrapper
├── .devtrace/                     # Project config
│   ├── configs/
│   │   └── local/
│   │       └── local_config.toml  # Credentials
│   └── hooks/                     # Git hooks
│       ├── prepare-commit-msg
│       ├── commit-msg
│       └── post-commit
├── tests/
├── docs/
└── README.md (this file)
```

### Running Commands

```bash
# Using uv run
uv run devtrace tickets

# Or build and use directly
uv build
```

### Testing

```bash
# Run tests
uv run pytest

# Lint code
uv run ruff check src/
```

---

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "FEAT: description"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## Security

**Credentials Handling**:

- Jira API tokens stored **locally** in `~/.devtrace/configs/local/`
- **Never** transmitted to DevTrace servers
- **Only** sent to Jira/GitHub APIs over HTTPS
- Automatically added to `.gitignore` to prevent accidental commits

**Best Practices**:

- Keep API tokens secret (treat like passwords)
- Revoke tokens if compromised
- Don't share config files with credentials

---

## Roadmap

### v0.2 (Next)

- [ ] GitHub Issues support
- [ ] React dashboard MVP
- [ ] Time tracking in CLI
- [ ] Bulk ticket operations

### v0.3

- [ ] Multi-account support
- [ ] Team metrics dashboard
- [ ] Slack integration
- [ ] Mobile app

### v0.4+

- [ ] AI-powered commit suggestions
- [ ] Custom workflow automation
- [ ] Cross-project tracking

---

## FAQ

**Q: Does DevTrace work with GitHub Issues?**  
A: Not yet. Currently Jira-focused. GitHub Issues support is planned for v0.2.

**Q: Can I use it with multiple Jira instances?**  
A: Not yet. Single instance per user. Multi-instance support planned for v0.3.

**Q: Are my credentials safe?**  
A: Yes. Stored locally in `~/.devtrace/configs/local/` and never transmitted to DevTrace servers.

**Q: Can I disable auto-comments?**  
A: Yes. Mark commits with `[WIP]` to skip auto-posting, or disable hooks with `git commit --no-verify`.

**Q: What if Jira is down?**  
A: Git commits still succeed. Hooks skip silently if Jira is unreachable.

See [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) for more FAQs.

---

## License

MIT License - See [LICENSE](./LICENSE) file

---

## Support

- **Issues**: [GitHub Issues](https://github.com/UtsavSingh315/devtrace-cli/issues)
- **Discussions**: [GitHub Discussions](https://github.com/UtsavSingh315/devtrace-cli/discussions)
- **Documentation**: See docs folder and markdown files in this repo

---

## Acknowledgments

- Built with ❤️ for developers who hate context-switching
- Inspired by real developer pain points
- Powered by Python, Jira, and Git

---

## Version

**Current**: v0.1.0 (Phase 1 & 2 Complete)  
**Status**: Production Ready (CLI + Hooks)  
**Last Updated**: March 27, 2026

---

**Ready to stop switching between Git and Jira?** Install DevTrace and experience seamless integration.

```bash
devtrace tickets
```
