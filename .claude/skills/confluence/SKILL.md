---
name: confluence
description: Document current work session in Confluence. Use when user types /confluence or asks to document their work.
allowed-tools: Read, Bash, Glob, Grep
---

# Confluence Work Logger

Documents work sessions and projects so others can understand and recreate them.

## When User Types /confluence

### Step 1: Determine Documentation Mode

Ask the user:
```
What are you documenting?
1. A specific task/ticket (work session documentation)
2. An entire project (comprehensive project documentation)
```

Store their answer as `doc_mode`.

---

## MODE 1: Ticket/Task Documentation (Work Session)

Use this mode when documenting a single work session, bug fix, feature implementation, or Jira ticket.

### Step 1A: Ask for Task Details

Ask:
```
What task are you documenting? (e.g., "Fixing authentication bug" or "Implementing user profile feature")
```

Store as `task_name`.

Ask:
```
Is this related to a Jira ticket? If yes, provide the ticket ID (e.g., PROJ-123). If no, just say "no".
```

Store as `jira_ticket_id` (or empty if not applicable).

### Step 2A: Fetch Jira Ticket Info (if applicable)

**If jira_ticket_id provided:**

Test Jira connection:
```bash
python .claude/skills/confluence/confluence_api.py test-jira-connection
```

Fetch ticket details:
```bash
python .claude/skills/confluence/confluence_api.py get-jira-issue --issue-key PROJ-123
```

Store the JSON response as `jira_info`.

### Step 3A: Gather Session Information

Look back through the conversation history and collect:

**What was done:**
- List key actions: code written, files modified, commands run, problems solved
- If they wrote a script, note what it does and its purpose
- Capture any important decisions or solutions

**Key information:**
- Files involved (list any files that were read, edited, or created)
- Commands run (any bash commands, installs, configurations)
- Code snippets (important functions or logic with proper language detection)
- Errors encountered and how they were fixed

### Step 4A: Generate Work Session Page

Use the `work_session_template()` function from `templates.py` to create the page content.

**Example usage:**
```python
from templates import work_session_template

content = work_session_template(
    task_name="Fix authentication timeout issue",
    overview="Fixed a bug where users were being logged out after 5 minutes instead of 30 minutes",
    actions_done=[
        "Identified the issue in session configuration",
        "Updated SESSION_TIMEOUT value in config.py",
        "Added unit tests for session timeout behavior",
        "Deployed to staging and verified fix"
    ],
    files_involved=[
        {"path": "config/settings.py", "description": "Updated SESSION_TIMEOUT from 300 to 1800"},
        {"path": "tests/test_auth.py", "description": "Added test_session_timeout test case"}
    ],
    code_snippets=[
        {
            "code": "SESSION_TIMEOUT = 1800  # 30 minutes in seconds",
            "language": "python",
            "title": "config/settings.py"
        }
    ],
    commands_run=[
        "pytest tests/test_auth.py",
        "python manage.py runserver"
    ],
    how_to_recreate=[
        "Open config/settings.py",
        "Locate SESSION_TIMEOUT constant",
        "Change value from 300 to 1800",
        "Run tests to verify: pytest tests/test_auth.py",
        "Deploy to staging"
    ],
    notes="The original value was likely a typo. Production already had the correct value.",
    errors_encountered="Initial tests failed because test database wasn't migrated. Fixed with: python manage.py migrate --database=test",
    jira_info=jira_info,  # Pass Jira info if available, otherwise None
    documented_by="Your Name"
)
```

Write this content to a temporary file (e.g., `/tmp/session_doc.html`).

### Step 5A: Create Confluence Page

**Page Title:** `[PROJ-123] task_name - YYYY-MM-DD` (or just `task_name - YYYY-MM-DD` if no Jira ticket)

**Check config:**
```bash
python .claude/skills/confluence/confluence_api.py test-connection
```

**Check for parent page (optional):**

Ask:
```
Is this a follow-up to a previous task? If yes, provide the parent page title. If no, just say "no".
```

If parent provided, search for it:
```bash
python .claude/skills/confluence/confluence_api.py search-page --title "Parent Task Title" --space Work
```

Get the `parent_page_id` from the response.

**Create the page:**
```bash
python .claude/skills/confluence/confluence_api.py create-page \
  --title "[PROJ-123] Fix authentication timeout - 2026-01-05" \
  --content-file /tmp/session_doc.html \
  --space Work \
  [--parent-id $parent_page_id]
```

### Step 6A: Link to Jira (if applicable)

**If Jira ticket provided:**

Add a comment to the Jira ticket with the Confluence page link:
```bash
python .claude/skills/confluence/confluence_api.py add-jira-comment \
  --issue-key PROJ-123 \
  --comment "Work session documented in Confluence: [page_url]"
```

### Step 7A: Show Result

Display to user:
```
✅ Work session documented in Confluence!

Page: [PROJ-123] Fix authentication timeout - 2026-01-05
URL: [page_url]

This documentation includes:
- What was done during this session
- Files modified and code changes
- Commands executed
- How to recreate the work
- Link to Jira ticket PROJ-123
```

---

## MODE 2: Project Documentation (Comprehensive)

Use this mode when documenting an entire project/codebase with multiple pages covering architecture, setup, dependencies, etc.

### Step 1B: Ask for Project Details

Ask:
```
What is the project name?
```

Store as `project_name`.

Ask:
```
Where is the project located? (provide the directory path)
```

Store as `project_path`.

### Step 2B: Analyze the Project

Use the allowed tools (Read, Bash, Glob, Grep) to gather information:

**Identify project type:**
- Look for package.json (Node.js), requirements.txt (Python), Cargo.toml (Rust), etc.
- Determine the main programming languages and frameworks

**Gather key information:**
- README files
- Configuration files
- Entry points (main.js, app.py, etc.)
- Directory structure
- Dependencies
- Build/run commands

### Step 3B: Generate Multiple Documentation Pages

Create the following pages using existing templates from `templates.py`:

1. **Project Overview** (parent page)
   - Use `project_overview_template()`
   - Include: project description, tech stack, metadata, quick start

2. **Architecture Overview** (child page)
   - Use `architecture_overview_template()`
   - Include: components, design patterns, data flow

3. **Dependencies** (child page)
   - Use `dependencies_template()`
   - List production and dev dependencies

4. **Setup & Installation** (child page)
   - Use `setup_installation_template()`
   - Prerequisites, installation steps, configuration

5. **Project Structure** (child page)
   - Use `project_structure_template()`
   - Directory tree and descriptions

6. **Key Files Reference** (child page)
   - Use `key_files_template()`
   - Document important files with code samples

### Step 4B: Create Pages in Confluence

**Check config:**
```bash
python .claude/skills/confluence/confluence_api.py test-connection
```

**Create parent page:**
```bash
python .claude/skills/confluence/confluence_api.py create-page \
  --title "MyProject Documentation" \
  --content-file /tmp/project_overview.html \
  --space Work
```

Store the `parent_page_id` from the response.

**Create child pages:**

For each child page:
```bash
python .claude/skills/confluence/confluence_api.py create-page \
  --title "Architecture Overview" \
  --content-file /tmp/architecture.html \
  --space Work \
  --parent-id $parent_page_id
```

### Step 5B: Show Result

Display to user:
```
✅ Project documentation created in Confluence!

Parent Page: MyProject Documentation
URL: [parent_page_url]

Child Pages Created:
- Architecture Overview
- Dependencies
- Setup & Installation
- Project Structure
- Key Files Reference

This documentation provides a comprehensive overview of the project for team members.
```

---

## Building Hierarchies

When users indicate this is a follow-up task or want to organize documentation hierarchically:

1. Search for the parent page by title
2. If found, use its `page_id` as `--parent-id` when creating the child page
3. The new page will appear under the parent in Confluence hierarchy

**Example hierarchy:**
```
Authentication System Refactor (parent)
├── Initial Analysis - 2026-01-05
├── Implementation - 2026-01-06
└── Testing & Deployment - 2026-01-07
```

Or for projects:
```
MyApp Project Documentation (parent)
├── Architecture Overview
├── Dependencies
├── Setup & Installation
├── Project Structure
└── Key Files Reference
```

---

## Tips for Good Documentation

**For Work Sessions (Mode 1):**
- Be specific about what was done in THIS session
- Include enough detail that someone else could follow along
- Capture error messages and solutions
- Note any "gotchas" or tricky parts
- Explain the "why" not just the "what"
- Keep it focused on this specific task

**For Projects (Mode 2):**
- Provide a high-level overview before diving into details
- Document the "why" behind architectural decisions
- Include setup instructions that actually work
- Keep documentation up-to-date with code changes
- Add diagrams where helpful (can be added manually later)

---

## Error Handling

- **Config missing:** Tell user to set up config.json (see config.md)
- **Connection fails:** Check config.json credentials
- **Parent page not found:** Offer to create as a standalone page instead
- **No conversation history:** Ask user to describe what they did
- **Jira connection fails:** Document without Jira integration, create page normally
- **Jira ticket not found:** Ask user to verify the ticket ID or proceed without Jira

---

## Language Detection for Code Snippets

When extracting code snippets, detect the language from:
- File extensions (.py, .js, .ts, .go, .java, .rs, etc.)
- File names (Dockerfile, Makefile, package.json, etc.)
- Context from the conversation

Common mappings:
- .py → python
- .js → javascript
- .ts → typescript
- .go → go
- .java → java
- .rs → rust
- .rb → ruby
- .sh → bash
- .sql → sql
- .yml, .yaml → yaml
- .json → json
- .xml → xml
- Dockerfile → dockerfile
