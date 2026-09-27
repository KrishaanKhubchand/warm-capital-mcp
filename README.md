# Warm Capital CRM — MCP Server

A Python MCP server (stdio transport) that wraps the Warm Capital CRM Convex HTTP API. Provides 6 tools for managing fundraising campaigns, pipeline contacts, notes, and tasks.

**No auth required.** Each MCP client spawns its own server instance via stdio.

## Quick Start

```bash
cd ~/warm-capital-mcp
pip install -e .       # or: uv pip install -e .
python3 server.py      # starts stdio MCP server
```

## Hermes Configuration

Add to `~/.hermes/config.yaml` under `mcp_servers`:

```yaml
mcp_servers:
  warm-capital:
    command: python3
    args:
      - /root/warm-capital-mcp/server.py
```

Then restart Hermes. The 6 tools will appear as `Mcp_warm-capital_*`.

## Codex Configuration

Add to your Codex MCP config (e.g. `~/.codex/mcp.json`):

```json
{
  "servers": {
    "warm-capital": {
      "command": "python3",
      "args": ["/path/to/warm-capital-mcp/server.py"]
    }
  }
}
```

## Tools Reference

### `get_campaigns`
- **Args:** none
- **Returns:** JSON array of all campaigns with stats, progress, and IDs.

### `get_pipeline`
- **Args:** `campaign_id` (string) — the campaign's Convex ID
- **Returns:** Full pipeline board — stages, contacts, amounts, next actions.

### `get_actions`
- **Args:** `campaign_id` (string)
- **Returns:** Task/action items organized by section (This Week, Next Week, Backlog).

### `move_contact`
- **Args:** `campaign_contact_id` (string), `new_stage` (string)
- **Returns:** Confirmation. Stage names: "Identified", "Intro Made", "Meeting Set", "Committed", "Received", "Passed", "Not Now".

### `add_note`
- **Args:** `contact_id` (string), `title` (string), `body?` (string), `type?` (string), `campaign_id?` (string)
- **Returns:** Confirmation. Types: note, email-sent, email-received, call, meeting, intro-made, intro-received, message, social.

### `create_task`
- **Args:** `section_id` (string), `title` (string), `status?` (string), `contact_id?` (string), `campaign_id?` (string), `description?` (string)
- **Returns:** Confirmation. Status: pending, done, cancelled.

## Campaign ID Reference

| Campaign | ID |
|---|---|
| Podcast Pipeline | `kx7b53k226ra9pbs0mcvw6f27d8f76x2` |
| Warm Angel Pipeline | `kx7cyc6p007hsqw3e0yax9ef9d8f76x2` |
| Connectors Pipeline | `kx75wp09cnecth2b663dm54c8h8f505d` |
| Targets Pipeline | `kx79h428zfet4wqyhabf8bsg5d8f49wf` |
| Feedback Ask — Cold Founders | `kx7cdqhzpd23xdfxk6y5vyzhzx8f75vd` |

## API Base URL

```
https://colorless-roadrunner-987.convex.site
```
