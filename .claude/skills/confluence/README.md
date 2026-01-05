# Confluence Work Logger

Document your work sessions so others can understand and recreate what you did.

## What It Does

When you're working on something (fixing an issue, writing a script, solving a problem), type `/confluence` and it will:

1. Ask what task you're documenting
2. Review what you did in this session
3. Create a Confluence page explaining:
   - What was done
   - How to recreate it
   - Code/scripts involved
   - Commands run
   - Important notes

Perfect for knowledge sharing and creating "how-to" docs from your actual work.

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
     "space_key": "DEV"
   }
   ```

4. **Install**:
   ```bash
   pip install requests
   ```

5. **Test**:
   ```bash
   python .claude/skills/confluence/confluence_api.py test-connection
   ```

## Usage Examples

### Example 1: Fixing Zscaler Issue

You spend an hour fixing Zscaler connectivity. When done, type:
```
/confluence
```

It asks: "What task are you documenting?"
You say: "Fixed Zscaler connection dropping on VPN"

It creates a Confluence page titled **"Fixed Zscaler connection dropping on VPN - 2026-01-05"** with:
- What the problem was
- What you changed
- Configuration files modified
- How others can apply the same fix

### Example 2: Writing a Script

You write a Python script to export data. Type:
```
/confluence
```

It asks: "What task are you documenting?"
You say: "Python script for daily data export"

It creates a page with:
- What the script does and why
- How to use it
- The full code with syntax highlighting
- Requirements and dependencies
- Example usage

### Example 3: Follow-up Task

Later you improve that script. Type:
```
/confluence
```

It asks: "Is this a follow-up to a previous task?"
You say: "Yes, parent is 'Python script for daily data export'"

It creates a child page under the original, building a tree:
```
Python script for daily data export
└── Added error handling and retry logic - 2026-01-06
```

## What Gets Documented

- **Actions taken**: Files created, edited, commands run
- **Code written**: Full scripts or important snippets
- **Problems solved**: Errors encountered and how you fixed them
- **How to recreate**: Step-by-step instructions
- **Context**: Why decisions were made, gotchas, tips

## Tree Organization

Create hierarchies for related tasks:

```
Zscaler Issue Resolution
├── Initial Investigation - 2026-01-05
├── Configuration Fix - 2026-01-05
└── Testing Results - 2026-01-06

Database Migration
├── Schema Changes - 2026-01-03
├── Data Migration Script - 2026-01-04
└── Rollback Procedure - 2026-01-04
```

## Files

- **SKILL.md** - Workflow Claude follows
- **confluence_api.py** - API client
- **templates.py** - Page formatting
- **config.json** - Your credentials (you create this)

## Team Sharing

Commit to git:
```bash
git add .claude/skills/confluence/
git commit -m "Add Confluence work logger"
```

**Don't commit**: `config.json` (already in .gitignore)

Each person creates their own `config.json` with their API token.

## Tips

- Document as you finish tasks, while it's fresh
- Be specific - others should be able to follow along
- Include error messages and solutions
- Explain "why" not just "what"
- For scripts, show example usage

## That's It!

Work on something → Type `/confluence` → Documentation created.

Simple, automatic knowledge sharing.
