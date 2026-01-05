# Confluence Work Logger

Document your work sessions and projects so others can understand and recreate what you did.

## What It Does

Type `/confluence` and choose between two modes:

### Mode 1: Ticket/Task Documentation (Work Session)
For documenting a single work session, bug fix, or feature:
- Links to Jira tickets automatically
- Documents what you did THIS session
- Creates a focused page with code, commands, and reproduction steps
- Perfect for daily work logs and ticket documentation

### Mode 2: Project Documentation (Comprehensive)
For documenting an entire project/codebase:
- Creates multiple organized pages (Overview, Architecture, Setup, etc.)
- Analyzes project structure and dependencies
- Generates comprehensive documentation hierarchy
- Perfect for onboarding and project handoffs

Both modes create searchable Confluence pages your team can reference.

## Setup (5 minutes)

1. **Copy config**:
   ```bash
   cp .claude/skills/confluence/config.json.example .claude/skills/confluence/config.json
   ```

2. **Get API token**: https://id.atlassian.com/manage/api-tokens

3. **Edit** `.claude/skills/confluence/config.json`:
   ```json
   {
     "confluence_url": "https://your-company.atlassian.net/wiki",
     "email": "your-email@example.com",
     "api_token": "your-token-here",
     "space_key": "DEV",
     "jira_url": "https://your-company.atlassian.net",
     "jira_project_key": "PROJ"
   }
   ```

   **Note**: `jira_url` and `jira_project_key` are optional. If provided, the skill will automatically link your work sessions to Jira tickets.

4. **Install**:
   ```bash
   pip install requests
   ```

5. **Test**:
   ```bash
   # Test Confluence connection
   python .claude/skills/confluence/confluence_api.py test-connection

   # Test Jira connection (optional, if you configured Jira)
   python .claude/skills/confluence/confluence_api.py test-jira-connection
   ```

## Usage Examples

### Mode 1: Ticket/Task Documentation

#### Example 1: Documenting a Jira Ticket

You just fixed a bug (ticket PROJ-123). Type:
```
/confluence
```

**Dialog:**
- "What are you documenting?" → Choose **1** (task/ticket)
- "What task?" → "Fixed authentication timeout issue"
- "Jira ticket ID?" → "PROJ-123"

**Result:** Creates **"[PROJ-123] Fixed authentication timeout issue - 2026-01-05"** with:
- Jira ticket panel (summary, status, priority, link)
- What was done
- Files modified with code snippets
- Commands executed
- How to recreate
- Comment added to Jira ticket with doc link

#### Example 2: Daily Work Log

You spent time investigating an issue without a ticket. Type:
```
/confluence
```

**Dialog:**
- "What are you documenting?" → Choose **1** (task/ticket)
- "What task?" → "Investigated memory leak in worker process"
- "Jira ticket ID?" → "no"

**Result:** Creates **"Investigated memory leak in worker process - 2026-01-05"** documenting your findings.

#### Example 3: Follow-up Work

Later you continue the investigation. Type:
```
/confluence
```

**Dialog:**
- "What are you documenting?" → Choose **1** (task/ticket)
- "What task?" → "Fixed memory leak in worker process"
- "Jira ticket ID?" → "PROJ-456"
- "Follow-up to previous task?" → "Yes, parent is 'Investigated memory leak in worker process'"

**Result:** Creates a child page under the original investigation.

### Mode 2: Project Documentation

#### Example 4: Documenting a Project

You want to document your entire REST API project. Type:
```
/confluence
```

**Dialog:**
- "What are you documenting?" → Choose **2** (entire project)
- "Project name?" → "Customer REST API"
- "Project location?" → "/Users/you/projects/customer-api"

**Result:** Creates a parent page **"Customer REST API Documentation"** with 5 child pages:
- Architecture Overview
- Dependencies
- Setup & Installation
- Project Structure
- Key Files Reference

Perfect for onboarding new team members!

## What Gets Documented

### For Work Sessions (Mode 1):
- **Jira ticket info**: Summary, status, priority, assignee (if provided)
- **Actions taken**: Files created, edited, commands run
- **Code written**: Full scripts or important snippets
- **Problems solved**: Errors encountered and how you fixed them
- **How to recreate**: Step-by-step instructions
- **Context**: Why decisions were made, gotchas, tips

### For Projects (Mode 2):
- **Overview**: Project description, purpose, tech stack
- **Architecture**: System components, design patterns, data flow
- **Dependencies**: Production and development dependencies with versions
- **Setup**: Prerequisites, installation steps, configuration examples
- **Structure**: Directory tree with descriptions of key directories
- **Key Files**: Important files with code samples and explanations

## Page Hierarchies

Both modes support hierarchical organization:

### Work Session Hierarchies (Mode 1):
```
Zscaler Issue Resolution
├── Initial Investigation - 2026-01-05
├── Configuration Fix - 2026-01-05
└── Testing Results - 2026-01-06

[PROJ-123] Authentication Refactor
├── [PROJ-123] Planning and Design - 2026-01-03
├── [PROJ-123] Implementation - 2026-01-04
└── [PROJ-123] Testing - 2026-01-05
```

### Project Documentation Hierarchies (Mode 2):
```
Customer REST API Documentation
├── Architecture Overview
├── Dependencies
├── Setup & Installation
├── Project Structure
└── Key Files Reference
```

## Files

- **SKILL.md** - Workflow Claude follows
- **confluence_api.py** - API client
- **templates.py** - Page formatting
- **config.json** - Your credentials (you create this)

## Manual CLI Commands

If you need to interact with Jira or Confluence directly without using the `/confluence` skill:

### Jira Commands

**Get ticket details:**
```bash
python .claude/skills/confluence/confluence_api.py get-jira-issue --issue-key PROJ-123
```

**Add comment to ticket:**
```bash
python .claude/skills/confluence/confluence_api.py add-jira-comment \
  --issue-key PROJ-123 \
  --comment "Updated documentation - see Confluence page"
```

**Test Jira connection:**
```bash
python .claude/skills/confluence/confluence_api.py test-jira-connection
```

### Confluence Commands

**Search for a page:**
```bash
python .claude/skills/confluence/confluence_api.py search-page \
  --title "My Page Title" \
  --space Work
```

**Update existing page:**
```bash
python .claude/skills/confluence/confluence_api.py update-page \
  --page-id 123456 \
  --title "Updated Title" \
  --content-file my_content.html
```

**Note:** The `/confluence` skill handles most of this automatically, but these commands are useful for scripting or manual operations.

## Team Sharing

Commit to git:
```bash
git add .claude/skills/confluence/
git commit -m "Add Confluence work logger"
```

**Don't commit**: `config.json` (already in .gitignore)

Each person creates their own `config.json` with their API token.

## Tips

### For Work Sessions (Mode 1):
- Document as you finish tasks, while it's fresh
- Be specific about what changed in THIS session
- Include error messages and how you solved them
- Explain "why" decisions were made, not just "what"
- Link to Jira tickets for context
- Use parent pages to group related work

### For Projects (Mode 2):
- Run this when starting a new project or when documentation is outdated
- Review generated docs and add diagrams manually if needed
- Keep architecture docs updated as the project evolves
- Use this for new team member onboarding
- Update setup instructions when dependencies change

## That's It!

**For daily work:**
Work on a ticket → Type `/confluence` → Choose Mode 1 → Work session documented with Jira link

**For projects:**
Have a codebase → Type `/confluence` → Choose Mode 2 → Complete project docs created

Simple, automatic knowledge sharing for both individual tasks and entire projects.
