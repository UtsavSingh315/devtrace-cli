# Phase 3: React Web Dashboard - Setup & Architecture

## Overview

Phase 3 builds a React web dashboard that provides a unified view of Jira tickets enriched with Git commit data. This "God-View" dashboard helps developers see:

- All their active tickets in one place
- Associated commits per ticket
- LOC changes (additions/deletions)
- Files modified
- Time tracking per ticket

---

## Technology Stack

- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite (fast, modern)
- **Styling**: Tailwind CSS (utility-first)
- **State Management**: React Context + Hooks
- **API Communication**: Fetch API + custom hooks
- **Data Visualization**:
  - Kanban board (react-beautiful-dnd or dnd-kit)
  - Charts (Recharts for LOC metrics)
- **Authentication**: Browser localStorage (local-first approach)

---

## Project Structure

```
devtrace-dashboard/
├── public/
│   └── favicon.svg
├── src/
│   ├── components/
│   │   ├── Layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Layout.tsx
│   │   ├── Auth/
│   │   │   ├── SetupForm.tsx          # Onboarding: Jira + GitHub creds
│   │   │   └── CredentialsModal.tsx
│   │   ├── Dashboard/
│   │   │   ├── TicketCard.tsx         # Individual ticket display
│   │   │   ├── TicketKanban.tsx       # Kanban board view
│   │   │   ├── TicketList.tsx         # Table/list view
│   │   │   └── GodView.tsx            # Main dashboard
│   │   ├── Ticket/
│   │   │   ├── TicketDetails.tsx      # Full ticket view
│   │   │   ├── CommitHistory.tsx      # Commits for a ticket
│   │   │   └── MetricsPanel.tsx       # LOC, files, time elapsed
│   │   └── Common/
│   │       ├── Badge.tsx
│   │       ├── Button.tsx
│   │       └── Card.tsx
│   ├── hooks/
│   │   ├── useJira.ts                 # Fetch Jira data
│   │   ├── useGitHub.ts               # Fetch GitHub data
│   │   ├── useAuth.ts                 # Manage credentials
│   │   └── useTickets.ts              # Combined Jira + Git data
│   ├── context/
│   │   ├── AuthContext.tsx            # Global auth state
│   │   └── TicketsContext.tsx         # Global tickets state
│   ├── services/
│   │   ├── jira.service.ts            # Jira API wrapper
│   │   ├── github.service.ts          # GitHub API wrapper
│   │   └── storage.service.ts         # localStorage abstraction
│   ├── types/
│   │   ├── index.ts                   # TypeScript interfaces
│   │   ├── Ticket.ts
│   │   └── Commit.ts
│   ├── utils/
│   │   ├── date.ts                    # Date formatting
│   │   ├── metrics.ts                 # LOC calculations
│   │   └── parser.ts                  # Parse ticket IDs from commits
│   ├── App.tsx
│   ├── App.css
│   └── main.tsx
├── index.html
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
├── package.json
└── .env.example
```

---

## Phase 3A: Onboarding & Setup View

### SetupForm Component

Users enter their credentials on first visit:

```
┌─────────────────────────────────────────────────┐
│         DevTrace Dashboard Setup                 │
├─────────────────────────────────────────────────┤
│                                                 │
│ Step 1: Jira Configuration                      │
│ ┌───────────────────────────────────────────┐  │
│ │ Host:      https://your-org.atlassian.net│  │
│ │ Email:     you@example.com                │  │
│ │ API Token: ••••••••••••••••••••••••••••   │  │
│ └───────────────────────────────────────────┘  │
│                                                 │
│ Step 2: GitHub Configuration                    │
│ ┌───────────────────────────────────────────┐  │
│ │ GitHub Token: ••••••••••••••••••••••••••  │  │
│ │ Username:     utsav-singh                 │  │
│ └───────────────────────────────────────────┘  │
│                                                 │
│            [Test Connection] [Save]            │
│                                                 │
│ 🔒 Credentials stored securely in browser      │
│    (localStorage, not transmitted to servers)   │
└─────────────────────────────────────────────────┘
```

**Features:**

- Input validation
- Test connection before saving
- Clear instructions for getting API tokens
- Option to save to browser localStorage or send to local backend

---

## Phase 3B: God-View Dashboard

Once authenticated, users see the unified dashboard:

```
┌──────────────────────────────────────────────────────────────────────┐
│ DevTrace   [Profile ▼]  [Settings ⚙]                         Search │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ 📊 Your Tickets (4 Open)     [Kanban] [List] [Timeline]             │
│                                                                      │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │
│ │ OPEN (2)     │  │ IN PROGRESS  │  │ IN REVIEW    │                │
│ ├──────────────┤  │ (1)          │  │ (1)          │                │
│ │              │  ├──────────────┤  ├──────────────┤                │
│ │ ┌──────────┐ │  │              │  │              │                │
│ │ │ DT-21    │ │  │ ┌──────────┐ │  │ ┌──────────┐ │                │
│ │ │ Jira API │ │  │ │ DT-25    │ │  │ │ DT-30    │ │                │
│ │ │          │ │  │ │ Add Docs │ │  │ │ UI Polish│ │                │
│ │ │ 3 commits│ │  │ │          │ │  │ │          │ │                │
│ │ │ +245,-18 │ │  │ │ 2 commits│ │  │ │ 1 commit │ │                │
│ │ └──────────┘ │  │ │ +89,-5   │ │  │ │ +12,-3   │ │                │
│ │              │  │ └──────────┘ │  │ │          │ │                │
│ │ ┌──────────┐ │  │              │  │ │ 🔗 Review│ │                │
│ │ │ DT-22    │ │  └──────────────┘  │ │ PR #456  │ │                │
│ │ │ Bug Fix  │ │                     │ └──────────┘ │                │
│ │ │          │ │                     └──────────────┘                │
│ │ │ 1 commit │ │                                                    │
│ │ │ +10,-8   │ │                                                    │
│ │ └──────────┘ │                                                    │
│ └──────────────┘                                                    │
│                                                                      │
│                                                                      │
│ Metrics Summary:                                                   │
│ ├─ Total LOC Written:  +356 lines                                 │
│ ├─ Total LOC Deleted:  -36 lines                                  │
│ ├─ Commits This Week:  7                                          │
│ └─ Avg Time per Ticket: 2.4 days                                  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Phase 3C: Data Integration (Jira + GitHub)

### Ticket Enrichment Pipeline

```
User Authenticates
  ↓
1. Fetch Jira Tickets (assigned to user)
  ├─ Key, Summary, Status, Priority
  ├─ Created, Updated, Due Date
  └─ Description
  ↓
2. For each ticket, parse for ticket ID in GitHub
  ├─ Search commits with ticket ID in message
  ├─ Fetch commit details (hash, message, author, date)
  └─ Calculate diff stats (additions, deletions)
  ↓
3. Match commits to tickets
  ├─ Extract ticket ID from commit message ([PROJ-123])
  ├─ Link commits to corresponding ticket
  └─ Aggregate metrics (total LOC, files touched, time elapsed)
  ↓
4. Display unified view
  ├─ Kanban board with enriched cards
  ├─ Metrics per ticket
  └─ Time tracking
```

### Data Model

```typescript
interface EnrichedTicket {
  // Jira fields
  key: string;
  summary: string;
  status: string;
  priority: string;
  created: Date;
  updated: Date;
  dueDate?: Date;
  description: string;

  // GitHub enrichment
  commits: Commit[];
  totalLOCAdded: number;
  totalLOCDeleted: number;
  filesModified: string[];

  // Calculated metrics
  timeElapsed?: number; // ms from first to last commit
  daysActive: number; // days since created
  commitCount: number;
}

interface Commit {
  hash: string;
  message: string;
  author: string;
  date: Date;
  files: FileChange[];
}

interface FileChange {
  filename: string;
  additions: number;
  deletions: number;
  changeType: "A" | "M" | "D" | "R"; // Added, Modified, Deleted, Renamed
}
```

---

## Implementation Steps

### Step 1: Initialize Vite Project

```bash
npm create vite@latest devtrace-dashboard -- --template react-ts
cd devtrace-dashboard
npm install
```

### Step 2: Install Dependencies

```bash
npm install \
  tailwindcss \
  postcss \
  autoprefixer \
  @tailwindcss/forms \
  @tailwindcss/typography \
  react-beautiful-dnd \
  recharts \
  axios \
  zod  # Type-safe API responses
```

### Step 3: Configure Tailwind

```bash
npx tailwindcss init -p
```

### Step 4: Create Core Services

1. **jira.service.ts** - Fetch tickets, details, post comments
2. **github.service.ts** - Search commits by ticket ID
3. **storage.service.ts** - Manage localStorage credentials

### Step 5: Build Components

1. SetupForm (onboarding)
2. GodView (main dashboard)
3. TicketCard (individual ticket display)
4. TicketKanban (kanban board)
5. MetricsPanel (LOC, time tracking)

### Step 6: Implement Data Hooks

1. `useJira()` - Fetch and cache Jira data
2. `useGitHub()` - Fetch and cache GitHub commits
3. `useTickets()` - Combine and enrich data

---

## API Integration Details

### Jira API Endpoints Used

```
GET  /rest/api/3/issues/search?jql=assignee=currentUser()
GET  /rest/api/3/issues/{key}
POST /rest/api/3/issues/{key}/comments
```

### GitHub API Endpoints Used

```
GET /repos/{owner}/{repo}/commits?q=message:{ticket-id}
GET /repos/{owner}/{repo}/commits/{sha}
```

### CORS Handling

Since Jira and GitHub APIs have CORS restrictions:

- Option 1: Use localStorage to store credentials and make requests from frontend (CORS-enabled APIs only)
- Option 2: Create a simple Node.js backend as a proxy

**Recommended**: Use Browser Extensions or local backend for CORS bypass during development.

---

## Example Component: TicketCard.tsx

```typescript
import React from 'react';
import { EnrichedTicket } from '../types';

interface TicketCardProps {
  ticket: EnrichedTicket;
  onClick?: () => void;
}

export const TicketCard: React.FC<TicketCardProps> = ({ ticket, onClick }) => {
  const locChange = `+${ticket.totalLOCAdded}, -${ticket.totalLOCDeleted}`;

  return (
    <div
      onClick={onClick}
      className="bg-white rounded-lg shadow p-4 cursor-pointer hover:shadow-lg transition-shadow"
    >
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-bold text-blue-600">{ticket.key}</h3>
        <span className={`px-2 py-1 rounded text-sm ${getStatusColor(ticket.status)}`}>
          {ticket.status}
        </span>
      </div>

      <h4 className="font-semibold text-gray-800 mb-3">{ticket.summary}</h4>

      <div className="text-sm text-gray-600 space-y-1 mb-3">
        <p>📝 {ticket.commitCount} commits</p>
        <p>📊 LOC: {locChange}</p>
        <p>📁 {ticket.filesModified.length} files</p>
      </div>

      {ticket.timeElapsed && (
        <p className="text-xs text-gray-500">
          ⏱️ {formatDuration(ticket.timeElapsed)}
        </p>
      )}
    </div>
  );
};
```

---

## Next: Implementation Order

1. ✅ **Phase 1** - CLI Jira Integration (COMPLETE)
2. ✅ **Phase 2** - Git Hooks (COMPLETE)
3. 🚀 **Phase 3A** - React Setup + Onboarding
4. 🚀 **Phase 3B** - God-View Dashboard
5. 🚀 **Phase 3C** - Data Integration & Metrics

---

## Stretch Goals

- Dark mode toggle
- Custom filters (by priority, status, team)
- Time tracking with timer widget
- Export metrics to PDF
- Slack integration for notifications
- Mobile-responsive design
