# 🚀 DevTrace - Getting Started in 5 Minutes

Welcome to DevTrace! This guide gets you up and running in 5 minutes.

---

## Step 1: Install (1 minute)

```bash
cd devtrace-cli
uv sync
```

**Verify Installation**:

```bash
uv run devtrace --help
```

You should see:

```
Usage: devtrace [OPTIONS] COMMAND [ARGS]...

Commands:
  hello     Say hello in style
  version   Show version
  init      Initialize devtrace project...
  ...
  tickets   Main tickets command
  tkt       View ticket details
  comment   Post comments to tickets
  hook      Git hook management
```

---

## Step 2: Configure Jira (2 minutes)

```bash
devtrace init jira
```

You'll be prompted for:

1. **Jira Host**: e.g., `https://your-org.atlassian.net`
2. **Email**: Your Jira account email
3. **API Token**: Get from https://id.atlassian.com/manage-profile/security/api-tokens

**Credentials are saved to**: `~/.devtrace/configs/local/local_config.toml`

---

## Step 3: See Your Tickets (1 minute)

```bash
devtrace tickets
```

You'll see a beautiful table of all your open Jira tickets:

```
📋 Your Jira Tickets (Status: Open)
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳────────────┳────────────┳──────────┳──────────┓
┃ Ticket │ Summary            ┃ Status    ┃ Created    ┃ Updated    ┃ Due Date ┃ Link     ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇════════════╇════════════╇══════════╇══════════┩
│ DT-21  │ Implement Jira API │ Open      │ 2026-02-20 │ 2026-03-27 │ 2026-04-15│ https...│
└────────┴────────────────────┴───────────┴────────────┴────────────┴──────────┴──────────┘
```

---

## Step 4: Set Your Active Ticket (1 minute)

Pick a ticket to work on:

```bash
devtrace start DT-21
```

This sets `DT-21` as your active ticket. Future commits will auto-post to this ticket.

---

## Step 5: Make a Commit & Watch the Magic! (1 minute)

```bash
git add .
git commit -m "implement new feature"
```

Behind the scenes:

1. ✅ **prepare-commit-msg** hook formats your message → `DT-21 | FEAT : implement new feature`
2. ✅ **commit-msg** hook validates the format
3. ✅ **post-commit** hook automatically posts to DT-21 on Jira

**Check the result**:

```bash
devtrace tkt DT-21
```

You'll see:

```
DT-21 — Implement Jira API Integration CLI Commands
Status: Open
Priority: High
...

💬 Recent Comments:

[1] DevTrace Bot (just now)
🤖 Automated DevTrace Update: Code committed
Commit: a3f8b2c
Files: src/main.py (+10, -2)
```

---

## 🎯 You're Done!

You now have:

| Feature                            | Status     |
| ---------------------------------- | ---------- |
| View your Jira tickets in terminal | ✅ Working |
| View full ticket details           | ✅ Working |
| Post comments to tickets           | ✅ Working |
| Auto-format commit messages        | ✅ Working |
| Auto-post commits to Jira          | ✅ Working |

---

## 📚 Next: Learn More

**View your ticket details**:

```bash
devtrace tkt DT-21
```

**Post a comment**:

```bash
devtrace comment "Ready for review"
```

**Switch to a different ticket**:

```bash
devtrace start DT-25
```

**See all open tickets with filters**:

```bash
devtrace tickets list --status "In Progress"
devtrace tickets list --limit 10
```

---

## ❓ Common Questions

### Q: Why did my commit message change?

**A**: DevTrace auto-formatted it! For example:

```
You typed:  "implement feature"
DevTrace became: "DT-21 | FEAT : implement feature"
```

This is by design—it ensures consistency and makes Jira tracking automatic.

### Q: Will my commits fail if Jira is down?

**A**: No! Git operations always succeed. Hooks are designed to augment, never block.

### Q: Can I disable auto-comments?

**A**: Yes! Mark as WIP to skip:

```bash
git commit -m "[WIP] experimental - don't report"
# Hook will skip posting
```

### Q: Where are my credentials stored?

**A**: In `~/.devtrace/configs/local/local_config.toml` (your home folder, not the project).

---

## 🎓 Full Documentation

Want to dive deeper? Check out:

- **[README.md](./README.md)** - Project overview
- **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** - Command cheat sheet
- **[JIRA_INTEGRATION.md](./JIRA_INTEGRATION.md)** - Phase 1 detailed guide
- **[GIT_HOOKS.md](./GIT_HOOKS.md)** - Phase 2 detailed guide
- **[PHASE_3_DASHBOARD.md](./PHASE_3_DASHBOARD.md)** - Dashboard (coming soon)

---

## 🚀 What's Next?

**For You**:

- Use DevTrace in your daily workflow
- Report any issues on GitHub
- Share feedback!

**For the Project**:

- Phase 3: React web dashboard is architected and ready to build
- Multi-account support planned
- GitHub Issues support coming soon

---

## 💡 Tips & Tricks

### Create Shell Aliases

Make commands shorter:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias dt='devtrace'
alias dtt='devtrace tickets'
alias dts='devtrace start'
alias dtc='devtrace comment'

# Now use:
dt tickets              # Same as: devtrace tickets
dts DT-21               # Same as: devtrace start DT-21
dtc "Ready for review"  # Same as: devtrace comment "..."
```

### View Multiple Statuses

```bash
devtrace tickets list --status "Done"
devtrace tickets list --status "In Progress"
```

### Check Your Daily Progress

```bash
# Morning: See what you need to work on
devtrace tickets list

# Evening: See what you accomplished
devtrace tickets list --status "Done"
```

---

## 🎉 Enjoy DevTrace!

You've successfully set up DevTrace and eliminated context-switching between Git and Jira.

**Happy coding!** 🚀

---

**Questions?** Check the docs or open an issue on GitHub.  
**Need help?** See [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) for FAQs.
