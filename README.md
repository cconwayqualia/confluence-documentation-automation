# Claude Code Confluence Work Logger

Automatically document your work sessions in Confluence. When you finish working on something (fixing bugs, writing scripts, solving problems), just ask Claude to document it and get a complete Confluence page with all the details.

## Features

- **5-minute setup** - Single JSON config file, no environment variables
- **Automatic documentation** - Claude reviews your work and creates formatted pages
- **Task hierarchies** - Organize related work into parent/child page trees
- **Code highlighting** - Syntax-highlighted code blocks in Confluence
- **Team ready** - Easy to share via git, each person uses their own API token

## Quick Start

### 1. Copy the config file
```bash
cp .claude/skills/confluence/config.json.example .claude/skills/confluence/config.json
```

### 2. Get your Confluence API token
1. Go to https://id.atlassian.com/manage/api-tokens
2. Click "Create API token"
3. Copy the token

### 3. Edit config.json
```json
{
  "confluence_url": "https://your-company.atlassian.net/wiki",
  "email": "your-email@example.com",
  "api_token": "your-token-here",
  "space_key": "Work"
}
```

### 4. Install dependencies
```bash
pip install requests
```

### 5. Test it
```bash
python .claude/skills/confluence/confluence_api.py test-connection
```

## Usage

When you finish working on something, just ask Claude:

```
Document this work in Confluence
```

Claude will ask what task you're documenting, then create a page with:
- Overview of what was done
- Files involved
- Code/scripts with syntax highlighting
- Step-by-step recreation instructions
- Notes and context

## Examples

### Bug Fix
**You say:** "Fixed Zscaler VPN connection issue"

**Claude creates:** Page titled "Fixed Zscaler VPN connection issue - 2026-01-05" with problem description, changes made, files modified, and how others can apply the fix.

### Script Documentation
**You say:** "Python script for daily data export"

**Claude creates:** Page with what the script does, how to use it, full code, requirements, and examples.

### Task Hierarchies
For follow-up work, Claude can create child pages under a parent task, building organized documentation trees.

## Files

- `.claude/skills/confluence/SKILL.md` - Main skill workflow
- `.claude/skills/confluence/confluence_api.py` - Confluence API client
- `.claude/skills/confluence/templates.py` - Page content templates
- `.claude/skills/confluence/config.json.example` - Config template
- `.claude/skills/confluence/config.md` - Setup guide
- `.claude/skills/confluence/README.md` - Usage docs

## Team Setup

### Share with your team
```bash
git clone https://github.com/yourusername/claude-confluence-skill
cd claude-confluence-skill
```

Each team member:
1. Copy `config.json.example` to `config.json`
2. Get their own API token
3. Fill in their credentials
4. Run `pip install requests`
5. Test: `python .claude/skills/confluence/confluence_api.py test-connection`

## Security

- ✅ `config.json` is in `.gitignore` (never committed)
- ✅ Each person uses their own API token
- ✅ No secrets in the code
- ⚠️ Rotate API tokens every 90 days

## Requirements

- Python 3.7+
- `requests` library
- Confluence Cloud instance
- Claude Code

## Documentation

See `.claude/skills/confluence/config.md` for detailed setup instructions and troubleshooting.

## License

MIT License - Feel free to use and modify
