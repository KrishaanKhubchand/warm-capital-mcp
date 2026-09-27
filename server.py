"""Warm Capital CRM — MCP Server (stdio transport).

Wraps the Convex HTTP API at colorless-roadrunner-987.convex.site.
No auth required. Run with: python3 server.py
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP
import httpx
import json

mcp = FastMCP("warm-capital-crm")

BASE_URL = "https://colorless-roadrunner-987.convex.site"

# ── Campaign ID reference ─────────────────────────────────────────────
CAMPAIGN_IDS = {
    "Podcast Pipeline": "kx7b53k226ra9pbs0mcvw6f27d8f76x2",
    "Warm Angel Pipeline": "kx7cyc6p007hsqw3e0yax9ef9d8f76x2",
    "Connectors Pipeline": "kx75wp09cnecth2b663dm54c8h8f505d",
    "Targets Pipeline": "kx79h428zfet4wqyhabf8bsg5d8f49wf",
    "Feedback Ask — Cold Founders": "kx7cdqhzpd23xdfxk6y5vyzhzx8f75vd",
}


@mcp.tool()
async def get_campaigns() -> str:
    """List all fundraising campaigns with stats and progress.

    Returns a JSON array of campaigns. Each campaign includes:
    - _id: the campaign ID (use this for get_pipeline / get_actions)
    - name: human-readable campaign name
    - stats: contact counts, amounts raised, stage breakdowns
    - progress: completion percentage and status

    Known campaign IDs:
      • Podcast Pipeline: kx7b53k226ra9pbs0mcvw6f27d8f76x2
      • Warm Angel Pipeline: kx7cyc6p007hsqw3e0yax9ef9d8f76x2
      • Connectors Pipeline: kx75wp09cnecth2b663dm54c8h8f505d
      • Targets Pipeline: kx79h428zfet4wqyhabf8bsg5d8f49wf
      • Feedback Ask — Cold Founders: kx7cdqhzpd23xdfxk6y5vyzhzx8f75vd
    """
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{BASE_URL}/api/campaigns")
        resp.raise_for_status()
        return resp.text


@mcp.tool()
async def get_pipeline(campaign_id: str) -> str:
    """Get the full pipeline board for a campaign.

    Args:
        campaign_id: The campaign's Convex document ID.
            Example: "kx7cyc6p007hsqw3e0yax9ef9d8f76x2" (Warm Angel Pipeline)

    Returns JSON with:
    - stages: ordered list of pipeline stages (e.g. "Identified", "Intro Made", "Meeting Set", "Committed", "Received")
    - contacts: all contacts in the pipeline with their current stage, check amounts, next actions, and notes
    - amounts: aggregated dollar amounts per stage

    Known campaign IDs:
      • Podcast Pipeline: kx7b53k226ra9pbs0mcvw6f27d8f76x2
      • Warm Angel Pipeline: kx7cyc6p007hsqw3e0yax9ef9d8f76x2
      • Connectors Pipeline: kx75wp09cnecth2b663dm54c8h8f505d
      • Targets Pipeline: kx79h428zfet4wqyhabf8bsg5d8f49wf
      • Feedback Ask — Cold Founders: kx7cdqhzpd23xdfxk6y5vyzhzx8f75vd
    """
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{BASE_URL}/api/pipeline/{campaign_id}")
        resp.raise_for_status()
        return resp.text


@mcp.tool()
async def get_actions(campaign_id: str) -> str:
    """Get task/action items for a campaign.

    Args:
        campaign_id: The campaign's Convex document ID.
            Example: "kx7cyc6p007hsqw3e0yax9ef9d8f76x2" (Warm Angel Pipeline)

    Returns JSON with tasks organized by section — e.g. "This Week", "Next Week",
    "Backlog". Each task has a title, status, optional contact link, and description.

    Known campaign IDs:
      • Podcast Pipeline: kx7b53k226ra9pbs0mcvw6f27d8f76x2
      • Warm Angel Pipeline: kx7cyc6p007hsqw3e0yax9ef9d8f76x2
      • Connectors Pipeline: kx75wp09cnecth2b663dm54c8h8f505d
      • Targets Pipeline: kx79h428zfet4wqyhabf8bsg5d8f49wf
      • Feedback Ask — Cold Founders: kx7cdqhzpd23xdfxk6y5vyzhzx8f75vd
    """
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{BASE_URL}/api/pipeline/{campaign_id}/actions")
        resp.raise_for_status()
        return resp.text


@mcp.tool()
async def move_contact(campaign_contact_id: str, new_stage: str) -> str:
    """Move a contact to a new pipeline stage.

    Args:
        campaign_contact_id: The campaign-contact junction ID (from get_pipeline results,
            the _id field on each contact entry — NOT the contact's own ID).
            Example: "kx7abc123..."
        new_stage: The target stage name. Must match an existing stage exactly.
            Common stages: "Identified", "Intro Made", "Meeting Set",
            "Committed", "Received", "Passed", "Not Now"

    Returns confirmation JSON on success.
    """
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{BASE_URL}/api/pipeline/contact/move",
            json={"campaignContactId": campaign_contact_id, "newStage": new_stage},
        )
        resp.raise_for_status()
        return resp.text


@mcp.tool()
async def add_note(
    contact_id: str,
    title: str,
    body: str = "",
    type: str = "note",
    campaign_id: str = "",
) -> str:
    """Log an interaction or note on a contact.

    Args:
        contact_id: The contact's Convex document ID.
        title: Short summary of the interaction (e.g. "Sent intro email", "Had coffee chat").
        body: Optional longer description or details.
        type: Interaction type. Defaults to "note". Options:
            • note — general note
            • email-sent — outbound email
            • email-received — inbound email
            • call — phone/video call
            • meeting — in-person or scheduled meeting
            • intro-made — you introduced this person to someone
            • intro-received — someone introduced you to this person
            • message — DM / text / WhatsApp
            • social — social media interaction
        campaign_id: Optional campaign ID to associate this note with a specific pipeline.

    Returns confirmation JSON on success.
    """
    payload: dict = {"contactId": contact_id, "title": title, "type": type}
    if body:
        payload["body"] = body
    if campaign_id:
        payload["campaignId"] = campaign_id

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{BASE_URL}/api/pipeline/contact/note",
            json=payload,
        )
        resp.raise_for_status()
        return resp.text


@mcp.tool()
async def create_task(
    section_id: str,
    title: str,
    status: str = "pending",
    contact_id: str = "",
    campaign_id: str = "",
    description: str = "",
) -> str:
    """Create a task/action item in a campaign's action board.

    Args:
        section_id: The section to add the task to (from get_actions results —
            each section has an _id). Sections are typically "This Week",
            "Next Week", "Backlog", etc.
        title: Task title (e.g. "Follow up with Sarah on intro", "Send deck to John").
        status: Task status. Defaults to "pending". Options: "pending", "done", "cancelled".
        contact_id: Optional contact ID to link this task to a specific person.
        campaign_id: Optional campaign ID to associate the task with.
        description: Optional longer description of the task.

    Returns confirmation JSON on success.
    """
    payload: dict = {"sectionId": section_id, "title": title, "status": status}
    if contact_id:
        payload["contactId"] = contact_id
    if campaign_id:
        payload["campaignId"] = campaign_id
    if description:
        payload["description"] = description

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{BASE_URL}/api/pipeline/task",
            json=payload,
        )
        resp.raise_for_status()
        return resp.text


if __name__ == "__main__":
    mcp.run()
