---
name: confluence
description: Document current work session in Confluence. Use when user types /confluence or asks to document their work.
allowed-tools: Read, Bash, Glob, Grep
---

# Confluence Work Logger

Documents what you're working on so others can understand and recreate it.

## When User Types /confluence

### Step 1: Ask What They're Working On

Ask the user:
```
What task are you documenting? (e.g., "Fixing Zscaler connection issue" or "Python script for data export")
```

Store their answer as `task_name`.

### Step 2: Ask If This is a Subtask

Ask:
```
Is this a follow-up to a previous task? If yes, what's the parent page title?
```

If they provide a parent page title, we'll search for it and make this a child page.

### Step 3: Gather Session Information

Collect from the conversation:

**What was done:**
- Look back through the conversation history
- List key actions: code written, files modified, commands run, problems solved
- If they wrote a script, note what it does and its purpose
- Capture any important decisions or solutions

**Key information:**
- Files involved (list any files that were read, edited, or created)
- Commands run (any bash commands, installs, configurations)
- Code snippets (important functions or logic)
- Errors encountered and how they were fixed

### Step 4: Generate Documentation Page

Create a Confluence page with this structure:

**Title:** `[task_name] - [date]`

**Content:**
```html
<h2>Overview</h2>
<p>[Brief summary of what this task was about]</p>

<h2>What Was Done</h2>
<ul>
  <li>[Action 1]</li>
  <li>[Action 2]</li>
  ...
</ul>

<h2>Key Files</h2>
<ul>
  <li><code>[file path]</code> - [what was done to it]</li>
</ul>

<h2>Code/Scripts</h2>
[Use code blocks for any important code]

<h2>Commands Run</h2>
[Code block with bash commands]

<h2>How to Recreate</h2>
<ol>
  <li>[Step 1]</li>
  <li>[Step 2]</li>
  ...
</ol>

<h2>Notes</h2>
<p>[Any important context, gotchas, or things to watch out for]</p>

<p><em>Documented by: [user] on [timestamp]</em></p>
```

Use the templates in `templates.py` to generate proper Confluence Storage Format HTML.

### Step 5: Create the Confluence Page

**Check config:**
```bash
python .claude/skills/confluence/confluence_api.py test-connection
```

If config missing or invalid, tell user to check their config.json.

**If this is a subtask:**
Search for parent page:
```bash
python .claude/skills/confluence/confluence_api.py search-page --title "Parent Task Title"
```

Get the parent_page_id.

**Create the page:**
```bash
python .claude/skills/confluence/confluence_api.py create-page \
  --title "[task_name] - [date]" \
  --content-file /tmp/session_doc.html \
  [--parent-id $parent_page_id]
```

### Step 6: Show Result

Display to user:
```
✅ Task documented in Confluence!

Page: [task_name] - [date]
URL: [page_url]

This documentation explains:
- What was done
- How to recreate it
- Key files and code involved
```

## For Scripts Specifically

If the task involves writing a script, make sure to include:
- **Purpose:** What the script does
- **Usage:** How to run it (with examples)
- **Parameters:** Any command-line args or config needed
- **Requirements:** Dependencies or prerequisites
- **Code:** The full script with syntax highlighting

## Building the Tree

When user says this is a subtask:
1. Search for the parent page by title
2. If found, use its page_id as --parent-id
3. The new page will appear under it in Confluence hierarchy
4. Update parent page to add a link to this new child (optional, but nice)

Example tree:
```
Zscaler Issue Resolution (parent)
├── Initial Investigation - 2026-01-05
├── Configuration Fix - 2026-01-05
└── Testing and Validation - 2026-01-06
```

## Tips for Good Documentation

- Be specific about what was done
- Include enough detail that someone else could follow along
- Capture error messages and solutions
- Note any "gotchas" or tricky parts
- For scripts, explain the "why" not just the "what"
- Keep it focused on this specific task

## Error Handling

- **Config missing:** Tell user to set up config.json (see config.md)
- **Connection fails:** Check config.json credentials
- **Parent page not found:** Offer to create this as a standalone page instead
- **No conversation history:** Ask user to describe what they did
