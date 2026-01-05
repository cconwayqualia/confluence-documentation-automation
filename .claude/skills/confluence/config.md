# Quick Setup

## 1. Copy the config file

```bash
cp .claude/skills/confluence/config.json.example .claude/skills/confluence/config.json
```

## 2. Get your API token

1. Go to https://id.atlassian.com/manage/api-tokens
2. Click "Create API token"
3. Copy the token

## 3. Edit config.json

Open `.claude/skills/confluence/config.json` and fill in:

```json
{
  "confluence_url": "https://your-company.atlassian.net/wiki",
  "email": "your-email@example.com",
  "api_token": "paste-your-token-here",
  "space_key": "DEV",
  "jira_url": "https://your-company.atlassian.net",
  "jira_project_key": "PROJ"
}
```

**Where to find these:**
- **confluence_url**: The URL you use to access Confluence (include `/wiki`)
- **email**: Your Atlassian/Confluence email
- **api_token**: The token from step 2 (same token works for both Confluence and Jira)
- **space_key**: The space where you want docs (look in Confluence URL: `/spaces/DEV/...`)
- **jira_url**: (Optional) Your Jira URL without `/wiki` suffix
- **jira_project_key**: (Optional) Default Jira project key (e.g., "PROJ", "DEV")

**Note:** If you don't use Jira, you can omit `jira_url` and `jira_project_key`. The skill will work fine without them.

## 4. Install Python library

```bash
pip install requests
```

## 5. Test it

```bash
# Test Confluence connection (required)
python .claude/skills/confluence/confluence_api.py test-connection

# Test Jira connection (optional, if you configured Jira)
python .claude/skills/confluence/confluence_api.py test-jira-connection
```

Both should say "Connection successful".

## Done!

Now just type `/confluence` in Claude Code to document work sessions or entire projects.

## Troubleshooting

- **Config file not found**: Did you copy config.json.example to config.json?
- **Authentication failed**: Check your email and API token are correct
- **Space not found**: Check your space_key (it's case-sensitive, usually uppercase)

## Security Note

Don't commit `config.json` to git! Add it to your `.gitignore`:

```
.claude/skills/confluence/config.json
```

The example file (`config.json.example`) is safe to commit.
