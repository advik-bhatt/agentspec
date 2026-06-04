"""
NYTechWeek Event Scout — ranks events by your interests using Claude.

Usage (live mode):  ANTHROPIC_API_KEY=sk-... python event_scout.py
Usage (demo mode):  python event_scout.py          # no key needed, deterministic output

AgentSpec feeds this agent a JSON payload via stdin:
  {"input": "<your interests>", "sources": [<event objects>]}
"""
from __future__ import annotations

import json
import os
import sys

payload = json.loads(sys.stdin.read())
interests: str = payload.get("input", "AI agents, developer tools, no hype")
sources: list[dict] = payload.get("sources", [])

api_key = os.getenv("ANTHROPIC_API_KEY")

if api_key:
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)

        events_block = "\n".join(
            f'- [{e["id"]}] {e.get("text", "")}' for e in sources
        )

        message = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"You are an event scout. Rank the following NYC Tech Week events "
                        f"for someone whose interests are: {interests}\n\n"
                        f"Events:\n{events_block}\n\n"
                        f"Return ONLY valid JSON with these fields:\n"
                        f"  ranked_events: list of event IDs in priority order\n"
                        f"  reasoning: one sentence per event explaining the ranking\n"
                        f"  citations: list of event IDs you referenced\n"
                        f"  tool_calls: [\"rank_events\"]\n"
                        f"Only reference events from the provided list. Do not invent events."
                    ),
                }
            ],
        )

        text = message.content[0].text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        result = json.loads(text)
        print(json.dumps(result))
        sys.exit(0)

    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)

else:
    # Demo mode — deterministic, no API key needed, still shows the contract passing
    event_ids = [e["id"] for e in sources]
    top = [eid for eid in event_ids if "agent" in eid.lower() or "ai" in eid.lower() or "dev" in eid.lower()]
    rest = [eid for eid in event_ids if eid not in top]
    ranked = top + rest

    result = {
        "ranked_events": ranked,
        "reasoning": (
            "Demo mode (set ANTHROPIC_API_KEY for live Claude ranking). "
            "AI/agent/dev events ranked first based on keyword match to interests."
        ),
        "citations": ranked[:3],
        "tool_calls": ["rank_events"],
    }
    print(json.dumps(result))
