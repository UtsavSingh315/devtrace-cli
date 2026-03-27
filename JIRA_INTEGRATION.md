# DevTrace Jira Integration - CLI Commands

## Overview

DevTrace integrates seamlessly with Jira to help developers manage tickets without leaving the terminal. All Jira interactions are authenticated via local TOML configuration stored at `~/.devtrace/configs/local/local_config.toml`.

## Setup

### 1. Initialize Jira Credentials

```bash
devtrace init jira
```

This interactive command will prompt you for:

- **Jira Host**: Your Atlassian instance URL (e.g., `https://your-org.atlassian.net`)
- **Email**: Your Jira account email
- **API Token**: Generate one at https://id.atlassian.com/manage-profile/security/api-tokens

Your credentials are stored locally and **not** committed to version control.

---

## Commands

### `devtrace tickets` - List Your Open Tickets

Fetch and display all Jira tickets currently assigned to you in a clean tabulated format.

**Usage:**

```bash
devtrace tickets list
devtrace tickets list --status "In Progress"
devtrace tickets list --limit 10
devtrace tickets  # Shorthand for 'list'
```

**Options:**

- `--status, -s`: Filter by status (default: "Open")
- `--limit, -l`: Maximum number of tickets to display

**Output Example:**

```
📋 Your Jira Tickets (Status: Open)
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳────────────┳────────────┳──────────┳──────────────┓
┃ Ticket │ Summary            ┃ Status      ┃ Created    ┃ Updated    ┃ Due Date ┃ Link         ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇════════════╇════════════╇══════════╇══════════════┩
│ DT-21  │ Implement Jira API │ Open        │ 2026-02-20 │ 2026-03-27 │ 2026-04-15│ https://...  │
└────────┴────────────────────┴─────────────┴────────────┴────────────┴──────────┴──────────────┘

✅ Showing 1 ticket(s)
```

---

### `devtrace tkt <ticket_id>` - View Ticket Details

Fetch and display the full details of a specific Jira ticket, including description, status, assignee, and recent comments.

**Usage:**

```bash
devtrace tkt DT-21
devtrace tkt PROJ-123 --no-comments
```

**Options:**

- `--comments/--no-comments`: Show or hide recent comments (default: show)

**Output Example:**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ DT-21 — Implement Jira API Integration CLI Commands   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Status: Open
Priority: High
Assignee: John Doe
Reporter: Jane Smith
Created: 2026-02-20 14:30
Updated: 2026-03-27 09:15
Due Date: 2026-04-15

📝 Description:
Implement comprehensive Jira API integration for the DevTrace CLI, including:
- Fetch user's open tickets
- View detailed ticket information
- Post comments to tickets
- Automated Git hook integration

💬 Recent Comments:

[1] John Doe (2026-03-27 09:15)
Great progress on Phase 1! All three commands are working well.

[2] Jane Smith (2026-03-26 15:45)
Make sure to handle edge cases with special characters in comments.

🔗 Open in Jira
```

---

### `devtrace comment "<message>"` - Post a Comment

Post a manual comment to the currently active Jira ticket or a specified ticket.

**Usage:**

```bash
devtrace comment "Fixed the critical bug"
devtrace comment "Updated tests" --ticket DT-25
devtrace comment "Merged to main" -t PROJ-456
```

**Options:**

- `--ticket, -t`: Target ticket ID (optional, uses active context if omitted)

**Output Example:**

```
📍 Using active ticket: DT-21
📝 Posting comment to DT-21...
✅ Comment posted successfully!
📌 Comment ID: 123456789
🔗 View in Jira
```

#### Active Ticket Context

If no `--ticket` is specified, DevTrace uses your currently active ticket from the local context. This is automatically set by:

```bash
devtrace start DT-21  # Set DT-21 as active ticket
devtrace comment "Working on this now"  # Posts to DT-21
```

---

## Configuration File

Your Jira credentials are stored in `~/.devtrace/configs/local/local_config.toml`:

```toml
[active]
ticket_id = "DT-21"
started_at = "2026-02-21T18:44:05.421753+05:30"
branch = "main"

[jira]
host = "https://your-org.atlassian.net"
email = "your-email@example.com"
api_token = "ATATT3xFfGF0_xxxxxxxxxxxxxxxxxxxxx"

[types]
allowed = ["FEAT", "FIX", "INIT", "DOCS", "REFACTOR", "TEST", "CHORE"]

[settings]
formater = true
```

**Security Note:** Never commit this file to version control. It's automatically added to `.gitignore`.

---

## Error Handling

All commands include robust error handling:

- **ConfigError**: Missing or invalid configuration
- **JiraError**: Jira API failures (authentication, network, etc.)

Example error output:

```
❌ Configuration Error: Missing Jira configuration keys: api_token
Please add these to your ~/.devtrace/configs/local/local_config.toml
```

---

## What's Next (Phase 2 & 3)

- **Phase 2**: Automated Git hooks to post commit messages to tickets
- **Phase 3**: React web dashboard with unified Jira + Git data
